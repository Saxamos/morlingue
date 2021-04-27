import sqlite3

import pandas as pd
import plotly_express as px
import streamlit as st

from morlingue import ROOT_PATH

st.set_page_config(
    page_title="Morlingue", page_icon=(ROOT_PATH.parent / "favicon.png").as_posix()
)
st.write(
    """
# 💰 Zamal's Morlingue 💰
"""
)


@st.cache(allow_output_mutation=True)
def connect():
    db_path = (ROOT_PATH.parent / "pythonsqlite.db").as_posix()
    return sqlite3.connect(db_path, check_same_thread=False)


def _init_asset(
        dataframe: pd.DataFrame,
        name: str,
        val: int,
        start_date: pd.Timestamp,
        kraken_val: int,
) -> pd.DataFrame:
    dataframe[name] = 0
    dataframe[name][dataframe["date"] > start_date] = val
    # add rows "date-1" & "date" for viz
    row = dataframe.iloc[-1, :].to_dict().copy()
    row["kraken_total"] = kraken_val
    row["date"] = start_date
    row[name] = 0
    dataframe = dataframe.append(row, ignore_index=True)
    row["date"] = start_date + pd.DateOffset(1)
    row[name] = val
    dataframe = dataframe.append(row, ignore_index=True)
    return dataframe


def _init_df() -> pd.DataFrame:
    # load from bdd
    dataframe = pd.read_sql_query("SELECT * FROM assets", connect())
    dataframe["date"] = pd.to_datetime(dataframe["date"])
    dataframe = dataframe.drop(columns=["id"], axis=1)

    # init values from the past
    dataframe = dataframe.append(
        {"date": pd.Timestamp(year=2016, month=9, day=1), "kraken_total": 500},
        ignore_index=True,
    )

    # init static values
    init_values = [
        {
            "name": "sax",
            "val": 6000,
            "start_date": pd.Timestamp(year=2018, month=9, day=1),
            "kraken_val": 5000,
        },
        {
            "name": "loan",
            "val": 13000,
            "start_date": pd.Timestamp(year=2019, month=4, day=1),
            "kraken_val": 10000,
        },
        {
            "name": "filly",
            "val": 2100,
            "start_date": pd.Timestamp(year=2020, month=7, day=1),
            "kraken_val": 10000,
        },
        {
            "name": "gold",
            "val": 10000,
            "start_date": pd.Timestamp(year=2020, month=9, day=1),
            "kraken_val": 10000,
        },
        {
            "name": "vieplus",
            "val": 12000,
            "start_date": pd.Timestamp(year=2020, month=11, day=1),
            "kraken_val": 11000,
        },
        {
            "name": "mg",
            "val": 21000,
            "start_date": pd.Timestamp(year=2020, month=12, day=20),
            "kraken_val": 30000,
        },
    ]
    for el in init_values:
        dataframe = _init_asset(dataframe, **el)

    return dataframe.sort_values(by=["date"])


df = _init_df()

kraken_total_df = df.set_index("date")["kraken_total"]
kraken_total_df.name = "kraken ₿"
fig = px.line(kraken_total_df, labels={"value": "€", "date": ""})

# TODO: dynamic
# df["metamask"] = 7959
# fig.add_scatter(x=df["date"], y=df["metamask"], mode="lines", name="ETH Ξ")
fig.add_scatter(x=df["date"], y=df["filly"], mode="lines", name="Filly 🐎")
fig.add_scatter(x=df["date"], y=df["loan"], mode="lines", name="RB's loan 🏦")
fig.add_scatter(x=df["date"], y=df["vieplus"], mode="lines", name="Vieplus 🏥")
fig.add_scatter(x=df["date"], y=df["mg"], mode="lines", name="MG 🏎️")
fig.add_scatter(x=df["date"], y=df["gold"], mode="lines", name="Gold 🥇")
fig.add_scatter(x=df["date"], y=df["sax"], mode="lines", name="Sax 🎷")
fig.add_scatter(x=df["date"], y=df.sum(axis=1), mode="lines", name="Total 💶")
st.plotly_chart(fig)

dataframe = pd.read_sql_query("SELECT * FROM crypto", connect())
dataframe["date"] = pd.to_datetime(dataframe["date"])
fig = px.line(x=dataframe["date"], y=dataframe["XXBT"], labels={"y": "€", "x": ""})
fig.add_scatter(x=dataframe["date"], y=dataframe["XLTC"])
fig.add_scatter(x=dataframe["date"], y=dataframe["XETH"])
st.plotly_chart(fig)
