import pandas as pd
import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
from utils import *


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
