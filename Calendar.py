import streamlit as st
from streamlit.logger import get_logger
from streamlit_gsheets import GSheetsConnection
from utils import *
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from dateutil.relativedelta import relativedelta


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



df_cal = get_calendar_df()
# st.dataframe(df_cal)
df_suche = df_cal[df_cal['Suche'] == True]
df_biete = df_cal[df_cal['Biete'] == True]
df_piv = df_cal.pivot(index='Name', columns='Date', values='Anwesend')
order = df.sort_values(by='Ankunft')["Name"]
order = list(order)
# df_piv = df_piv.sort_values(by='Name', key=lambda x: order.index(x))
df_piv = df_piv.reindex(order)


column_map = {}
cols = df_piv.columns
for col in cols:
    split = str(col).split("-")
    column_map[col] = split[2] + "." + split[1]
df_piv.rename(columns=column_map, inplace=True)

df_piv_suche = df_suche.pivot(index='Name', columns='Date', values='Suchend')
df_piv_biete = df_biete.pivot(index='Name', columns='Date', values='Bietend')


def highlight_cells_green(value):
    if value:
        return 'background-color: green'
    else:
        return ''

def highlight_cells_orange(value):
    if value:
        return 'background-color: orange'
    else:
        return ''

def highlight_cells_blue(value):
    if value:
        return 'background-color: lightblue'
    else:
        return ''

styled_df = df_piv.style.applymap(highlight_cells_green)
styled_df_suche = df_piv_suche.style.applymap(highlight_cells_orange)
styled_df_biete = df_piv_biete.style.applymap(highlight_cells_blue)

stdf_anwesend = st.dataframe(styled_df)

with st.expander("Personen, die noch eine Unterkunft suchen:"):
    if not df_piv_suche.empty:
        stdf_suchen = st.dataframe(styled_df_suche)
    else:
        st.error("Es werden zurzeit keine Unterkünfte gesucht")

with st.expander("Personen, die eine Unterkunft anbieten:"):
    if not df_piv_biete.empty:
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
    print(row)
    print()
    submit_registration(row)
    st.rerun()