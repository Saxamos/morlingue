import sqlite3

import pandas as pd
import plotly_express as px
import streamlit as st

from morlingue import ROOT_PATH

st.write(
    """
# 💰 Zamal's Morlingue 💰
"""
)


@st.cache(allow_output_mutation=True)
def connect():
    db_path = (ROOT_PATH.parent / "pythonsqlite.db").as_posix()
    return sqlite3.connect(db_path, check_same_thread=False)


def _init_asset(dataframe: pd.DataFrame, name: str, val: int, start_date: pd.Timestamp) -> pd.DataFrame:
    dataframe[name] = 0
    dataframe[name][dataframe["date"] > start_date] = val
    return dataframe


def _init_df() -> pd.DataFrame:
    # load from bdd
    dataframe = pd.read_sql_query("SELECT * FROM assets", connect())
    dataframe["date"] = pd.to_datetime(dataframe["date"])

    # init values from the past
    dataframe = dataframe.append(
        {"date": pd.Timestamp(year=2016, month=9, day=1), "kraken_total": 500},
        ignore_index=True,
    )
    dataframe = dataframe.append(
        {"date": pd.Timestamp(year=2020, month=12, day=20), "kraken_total": 30000},
        ignore_index=True,
    )
    dataframe = dataframe.append(
        {"date": pd.Timestamp(year=2020, month=12, day=21), "kraken_total": 30000},
        ignore_index=True,
    )
    dataframe = dataframe.sort_values(by=["date"])

    # init static values
    dataframe = _init_asset(dataframe, "filly", 2100, pd.Timestamp(year=2020, month=7, day=1))
    dataframe = _init_asset(dataframe, "mg", 21000, pd.Timestamp(year=2020, month=12, day=20))
    dataframe = _init_asset(dataframe, "vieplus", 12000, pd.Timestamp(year=2020, month=11, day=1))
    dataframe = _init_asset(dataframe, "loan", 13000, pd.Timestamp(year=2019, month=4, day=1))
    dataframe = _init_asset(dataframe, "gold", 10000, pd.Timestamp(year=2020, month=9, day=1))
    dataframe = _init_asset(dataframe, "sax", 6000, pd.Timestamp(year=2018, month=9, day=1))

    return dataframe


df = _init_df()

kraken_total_df = df.set_index("date")["kraken_total"]
kraken_total_df.name = "kraken ₿"
fig = px.line(kraken_total_df, labels={"value": "€", "date": ""})

# TODO: dynamic
df["metamask"] = 7959
fig.add_scatter(x=df["date"], y=df["metamask"], mode="lines", name="ETH Ξ")
fig.add_scatter(x=df["date"], y=df["filly"], mode="lines", name="Filly 🐎")
fig.add_scatter(x=df["date"], y=df["loan"], mode="lines", name="RB's loan 🏦")
fig.add_scatter(x=df["date"], y=df["vieplus"], mode="lines", name="Vieplus 🏥")
fig.add_scatter(x=df["date"], y=df["mg"], mode="lines", name="MG 🏎️")
fig.add_scatter(x=df["date"], y=df["gold"], mode="lines", name="Gold 🥇")
fig.add_scatter(x=df["date"], y=df["sax"], mode="lines", name="Sax 🎷")

fig.add_scatter(x=df["date"], y=df.sum(axis=1), mode="lines", name="Total 💶")
st.plotly_chart(fig)
