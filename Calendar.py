import streamlit as st
from streamlit.logger import get_logger
from streamlit_gsheets import GSheetsConnection
from utils import *
import plotly.express as px

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

fig_anwesenheit = get_timeline(df, "Ankunft", "Abreise", "Anwesenheit")
px_anwesenheit = st.plotly_chart(fig_anwesenheit, use_container_width=True, height=500)

with st.expander("Suche Schlafplatz"):
    df_suche = df[df['Suche'] == True]
    if not df_suche.empty:
        fig_suche = get_timeline(df_suche, "SucheAb", "SucheBis", "Suche Schlafplatz")
        px_suche = st.plotly_chart(fig_suche, use_container_width=True, height=500)
    else:
        st.error("Es werden keine Schlafplätze gesucht")

with st.expander("Biete Schlafplatz"):
    df_biete = df[df['Biete'] == True]
    if not df_biete.empty:
        fig_biete = get_timeline(df_biete, "BieteAb", "BieteBis", "Biete Schlafplatz")
        px_biete = st.plotly_chart(fig_biete, use_container_width=True, height=500)
    else:
        st.error("Es werden keine Schlafplätze angeboten")