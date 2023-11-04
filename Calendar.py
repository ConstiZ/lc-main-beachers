import streamlit as st
from streamlit.logger import get_logger
from streamlit_gsheets import GSheetsConnection
from utils import *
LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Los Cristianos '24",
        page_icon="🏐",
    )

    st.title("Los Cristianos '24")

    # st.sidebar.success("Select a demo above.")

    

if __name__ == "__main__":
    run()


df_calendar = get_calendar_df()
st_df = st.dataframe(df_calendar)
