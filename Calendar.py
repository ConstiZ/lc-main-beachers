import streamlit as st
from streamlit.logger import get_logger
from streamlit_gsheets import GSheetsConnection
from utils import *
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from dateutil.relativedelta import relativedelta
from datetime import date

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Los Cristianos '24",
        page_icon="🏐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Los Cristianos '24")

    # st.sidebar.success("Select a demo above.")


if __name__ == "__main__":
    run()


df = get_df(get_worksheet())

day = date.today()
with st.expander("Stats - Heute " + str(day.strftime("%d.%m.%Y")), expanded=False):
    col1, col2, col3 = st.columns(3)
    
    # Metric Cards
    with col1:
        df_met, _ = get_calendars_piv(df, 'Anwesend', start_date, end_date)
        # Gesamt
        st.metric("Gesamtanmeldungen", df.shape[0])

    # daily
    # with col2:
        day_met = get_attendance(df, day)
        day_met_prev = get_attendance(df, day - datetime.timedelta(days=1))
        st.metric("Anwesenheit heute " + str(day.strftime("%d.%m.%Y")), day_met, day_met - day_met_prev)
    
    with col2:
        day_end = day + datetime.timedelta(days=7)
        df_arrivals = get_arrivals(df, "Ankunft", day, day_end)
        st.write("Ankunft - nächste 7 Tage")
        st.dataframe(df_arrivals)

    with col3:
        day_end = day + datetime.timedelta(days=7)
        df_arrivals = get_arrivals(df, "Abreise", day, day_end)
        st.write("Abreise - nächste 7 Tage")
        st.dataframe(df_arrivals)


st_slider = st.slider(
    "Zeitraum",
    value=(date.today()     , end_date), format="DD.MM.YYYY")
df_cal, styled_df = get_calendars_piv(df, 'Anwesend', st_slider[0], st_slider[1])
df_cal_suche, styled_df_suche = get_calendars_piv(df, 'Suchend', st_slider[0], st_slider[1])
df_cal_biete, styled_df_biete = get_calendars_piv(df, 'Bietend', st_slider[0], st_slider[1])


# streamlit

stdf_anwesend = st.dataframe(styled_df)

with st.expander("Personen, die noch eine Unterkunft suchen:"):
    if not df_cal_suche.empty:
        stdf_suchen = st.dataframe(styled_df_suche)
    else:
        st.error("Es werden zurzeit keine Unterkünfte gesucht")

with st.expander("Personen, die eine Unterkunft anbieten:"):
    if not df_cal_biete.empty:
        stdf_biete = st.dataframe(styled_df_biete)
    else:
        st.error("Es werden zurzeit keine Unterkünfte angeboten")




st.markdown("---")
st.header("Anmelden")

first_name = st.text_input("Vorname")
last_name = st.text_input("Nachname")
city = st.text_input("Stadt")

today = datetime.datetime.now()
next_month = today + relativedelta(months=1)


d_stay = st.date_input(
    "Ankunft - Abreise",
    (start_date, next_month),
    start_date,
    end_date,
    format="DD.MM.YYYY",
)

cb_lf = st.checkbox("Suche Unterkunft")
if cb_lf:
    d_lf = st.date_input(
        "Suche Unterkunft für diesem Zeitraum",
        (start_date, next_month),
        start_date,
        end_date,
        format="DD.MM.YYYY",
    )

cb_offer = st.checkbox("Biete Unterkunft")
if cb_offer:
    d_offer = st.date_input(
        "Biete Unterkunft für diesem Zeitraum",
        (start_date, next_month),
        start_date,
        end_date,
        format="DD.MM.YYYY",
    )

if isinstance(d_stay, tuple) and len(d_stay) > 1:
    row = {
        "Vorname": first_name,
        "Nachname": last_name,
        "Stadt": city,
        "Ankunft": d_stay[0],
        "Abreise": d_stay[1],
        "Suche": cb_lf,
        "Biete": cb_offer,
    }
if cb_offer and isinstance(d_offer, tuple) and len(d_offer) > 1:
    row["BieteAb"] = d_offer[0] if cb_offer else None
    row["BieteBis"] = d_offer[1] if cb_offer else None
if cb_lf and isinstance(d_lf, tuple) and len(d_lf) > 1:
    row["SucheAb"] = d_lf[0] if cb_lf else None
    row["SucheBis"] = d_lf[1] if cb_lf else None


b_submit = st.button("Submit")
if b_submit:
    submit_registration(row)
    st.rerun()