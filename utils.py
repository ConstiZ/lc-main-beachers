import pandas as pd

import streamlit as st

from streamlit_gsheets import GSheetsConnection
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import streamlit as st
import datetime

columns = ["Vorname", "Nachname", "Stadt", "Ankunft", "Abreise", "Suche", "SucheAb", "SucheBis", "Biete", "BieteAb", "BieteBis"]
start_date = datetime.date(2023, 11, 1)
end_date = datetime.date(2024, 4, 1)

def get_worksheet():
    credentials = dict(st.secrets["service_account_json"]["json"])
    url = st.secrets["connection"]["gsheets"]["spreadsheet"]
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(url)
    return sh.get_worksheet(0)


def get_df(worksheet):
    df = get_as_dataframe(worksheet)
    df = df[columns]
    df = df.dropna(how='all')
    df = df.reset_index(drop=True)
    return df

def submit_registration(row):
    worksheet = get_worksheet()
    df = get_df(worksheet)
    df_row = pd.DataFrame([row])
    # drop old row
    condition = (df["Vorname"] == row["Vorname"]) & (df["Nachname"] == row["Nachname"])
    if condition.any():
        st.info("Daten aktualisiert")
    st.success("Daten gespeichert")

    df = df.drop(df[condition].index)
    df = df.append(df_row)
    set_with_dataframe(worksheet, df)


def get_calendar_df():
    df = get_df(get_worksheet())

    # make date list
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)
    
    df_date = pd.DataFrame(date_list, columns=["Date"])

    df_calendar = df.merge(df_date, how="cross")
    return df_calendar