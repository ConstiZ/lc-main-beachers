import streamlit as st
from streamlit.logger import get_logger
from streamlit_gsheets import GSheetsConnection
from utils import *
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder



LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Los Cristianos '24",
        page_icon="🏐",
        layout="wide"
    )

    st.title("Los Cristianos '24")

    # st.sidebar.success("Select a demo above.")


if __name__ == "__main__":
    run()


df = get_df(get_worksheet())



df_cal = get_calendar_df()
df_suche = df_cal[df_cal['Suche'] == True]
df_biete = df_cal[df_cal['Biete'] == True]

df_piv = df_cal.pivot(index='Name', columns='Date', values='Anwesend')
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

