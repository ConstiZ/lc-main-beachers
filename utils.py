import pandas as pd

import streamlit as st

from streamlit_gsheets import GSheetsConnection
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import streamlit as st
import datetime
import plotly.express as px


columns = [
    "Vorname",
    "Nachname",
    "Stadt",
    "Ankunft",
    "Abreise",
    "Suche",
    "SucheAb",
    "SucheBis",
    "Biete",
    "BieteAb",
    "BieteBis",
]
start_date = datetime.date(2023, 12, 16)
end_date = datetime.date(2024, 4, 1)


def get_timeline(df, start, end, title, y="Name"):
    fig = px.timeline(df, x_start=start, x_end=end, y=y, title=title)
    fig.update_yaxes(
        categoryorder="total ascending"
    )  # Order tasks by their position in the DataFrame

    # Customize the x-axis tick values and labels
    date_range = pd.date_range(start=df[start].min(), end=df[end].max())
    fig.update_xaxes(
        tickvals=date_range,  # Specify the tick values (every day)
        ticktext=[
            date.strftime("%d.%m.%Y") for date in date_range
        ],  # Format the tick labels
        tickmode="array",
    )
    fig.update_layout(height=600)
    fig.update_xaxes(nticks=14, showgrid=True, tickmode="linear")

    return fig


def get_worksheet():
    credentials = dict(st.secrets["service_account_json"]["json"])
    url = st.secrets["connection"]["gsheets"]["spreadsheet"]
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(url)
    return sh.get_worksheet(0)


def get_df(worksheet):
    df = get_as_dataframe(worksheet)
    df = df[columns]
    df = df.dropna(how="all")
    df = df.reset_index(drop=True)
    dates = ["Ankunft", "Abreise", "SucheAb", "SucheBis", "BieteAb", "BieteBis"]
    for d in dates:
        df[d] = pd.to_datetime(df[d])
    bools = ["Suche", "Biete"]
    for b in bools:
        df[b] = df[b].astype(bool)

    df["Name"] = df["Vorname"] + " " + df["Nachname"]
    df = df.sort_values(by="Ankunft")
    return df


def submit_registration(row):
    worksheet = get_worksheet()
    df = get_df(worksheet)
    df_row = pd.DataFrame([row])
    if (
        row["Vorname"] is None
        or row["Vorname"] == ""
        or row["Nachname"] is None
        or row["Nachname"] == ""
    ):
        st.error("Bitte Vor- & Nachname eingeben")
        return False
    # drop old row
    condition = (df["Vorname"] == row["Vorname"]) & (df["Nachname"] == row["Nachname"])
    if condition.any():
        st.info("Daten aktualisiert")
    st.success("Daten gespeichert")

    df = df.drop(df[condition].index)
    df = df.append(df_row)
    set_with_dataframe(worksheet, df)
    return True


def get_calendar_df(df, start_date, end_date):
    # make date list
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)

    df_date = pd.DataFrame(date_list, columns=["Date"])

    df_calendar = df.merge(df_date, how="cross")
    df_calendar["Anwesend"] = (df_calendar["Ankunft"] <= df_calendar["Date"]) & (
        df_calendar["Date"] <= df_calendar["Abreise"]
    )
    df_calendar["Suchend"] = (df_calendar["SucheAb"] <= df_calendar["Date"]) & (
        df_calendar["Date"] <= df_calendar["SucheBis"]
    )
    df_calendar["Bietend"] = (df_calendar["BieteAb"] <= df_calendar["Date"]) & (
        df_calendar["Date"] <= df_calendar["BieteBis"]
    )

    def lambda_row(a, s, b):
        x = ""
        if a:
            x = "A"
        if s:
            x += "S"
        if b:
            x += "b"
        return x

    df_calendar["Status"] = df_calendar.apply(
        lambda row: lambda_row(row["Anwesend"], row["Suchend"], row["Bietend"]), axis=1
    )

    return df_calendar


def get_calendars_piv(
    df,
    col_value="Anwesend",
    start_date=datetime.date(2023, 12, 16),
    end_date=datetime.date(2024, 4, 1),
):
    map_sort = {"Anwesend": "Ankunft", "Suchend": "SucheAb", "Bietend": "BieteAb"}
    map_style = {
        "Anwesend": highlight_cells_green,
        "Suchend": highlight_cells_orange,
        "Bietend": highlight_cells_blue,
    }
    sort_col = map_sort[col_value]

    df_cal_all = get_calendar_df(df, start_date, end_date)

    # filter
    df_cal = df_cal_all[
        df_cal_all.apply(
            lambda row: row[col_value]
            and row["Date"] >= start_date
            and row["Date"] <= end_date,
            axis=1,
        )
    ]

    # sort
    order = df.sort_values(by=map_sort[col_value])["Name"]
    order = list(order)
    order = [x for x in order if x in df_cal["Name"].values]

    df_piv = df_cal.pivot(index="Name", columns="Date", values=col_value)
    df_piv = df_piv.reindex(order)

    column_map = {}
    cols = df_piv.columns
    for col in cols:
        split = str(col).split("-")
        column_map[col] = split[2] + "." + split[1]
    df_piv.rename(columns=column_map, inplace=True)

    styled_df = df_piv.style.applymap(map_style[col_value])

    return df_piv, styled_df


def highlight_cells_green(value):
    if not pd.isna(value):
        return "background-color: green"
    else:
        return ""


def highlight_cells_orange(value):
    if not pd.isna(value):
        return "background-color: orange"
    else:
        return ""


def highlight_cells_blue(value):
    if not pd.isna(value):
        return "background-color: lightblue"
    else:
        return ""


def get_attendance(df, day):
    df_ = df[(df["Ankunft"].dt.date <= day) & (df["Abreise"].dt.date >= day)].shape[0]
    return df_
    


def get_arrivals(df, col, start, end):
    df_ = df[(df[col].dt.date >= start) & (df[col].dt.date <= end)]
    df_[col] = pd.to_datetime(df_[col])
    if not df_.empty:
        df_[col + " in"] = (df_[col].dt.date - start).dt.days
    else:
        df_[col + " in"] = None
    columns = ["Name", "Stadt", col + " in", col]
    df_= df_[columns]
    df_ = df_.sort_values(by=col + " in", ascending=True)
    df_ = df_.set_index(df_.columns[0])
    df_[col] = pd.to_datetime(df_[col]).dt.strftime('%d.%m.%Y')
    return df_