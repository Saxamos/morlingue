import sqlite3

import pandas as pd
import plotly_express as px
import streamlit as st

from morlingue import ROOT_PATH

st.write(
    """
# Zamal's Morlingue 💸
*Kraken assets*
"""
)


@st.cache(allow_output_mutation=True)
def connect():
    return sqlite3.connect(ROOT_PATH.parent / "pythonsqlite.db", check_same_thread=False)


df = pd.read_sql_query("SELECT * FROM assets", connect())
df["date"] = pd.to_datetime(df["date"])

kraken_total_df = df.set_index("date")["kraken_total"]
kraken_total_fig = px.line(kraken_total_df, labels={"value": "€", "date": ""})
st.plotly_chart(kraken_total_fig)
