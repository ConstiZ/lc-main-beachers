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

# fig_anwesenheit = get_timeline(df, "Ankunft", "Abreise", "Anwesenheit")
# px_anwesenheit = st.plotly_chart(fig_anwesenheit, use_container_width=True, height=500)

# with st.expander("Suche Schlafplatz"):
#     df_suche = df[df['Suche'] == True]
#     if not df_suche.empty:
#         fig_suche = get_timeline(df_suche, "SucheAb", "SucheBis", "Suche Schlafplatz")
#         px_suche = st.plotly_chart(fig_suche, use_container_width=True, height=500)
#     else:
#         st.error("Es werden keine Schlafplätze gesucht")

# with st.expander("Biete Schlafplatz"):
#     df_biete = df[df['Biete'] == True]
#     if not df_biete.empty:
#         fig_biete = get_timeline(df_biete, "BieteAb", "BieteBis", "Biete Schlafplatz")
#         px_biete = st.plotly_chart(fig_biete, use_container_width=True, height=500)
#     else:
#         st.error("Es werden keine Schlafplätze angeboten")


df_cal = get_calendar_df()


gb = GridOptionsBuilder()

# makes columns resizable, sortable and filterable by default
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)

#configures Power Plant column to have a tooltip and adjust to fill the grid container
gb.configure_column(
    field="Name",
    header_name="Name",
    flex=1,
    tooltipField="Name",
    rowGroup=True
)

gb.configure_column(
    field="Date",
    header_name="Date",
    width=100,
    #valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
    pivot=True # this tells the grid we'll be pivoting on reference date
)

gb.configure_column(
    field="Status",
    header_name="Status",
    width=100,
    #type=["numericColumn"],
    #valueFormatter="value.toLocaleString()",
    aggFunc="first" # this tells the grid we'll be summing values on the same reference date
)

#makes tooltip appear instantly
gb.configure_grid_options(
    pivotMode=True # Enables pivot mode
    )
go = gb.build()

AgGrid(df_cal, gridOptions=go, height=400)