import sqlite3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from morlingue import ROOT_PATH, HOUR

COLORS = {"background": "lightslategray", "line": "darkslategray", "text": "lightcyan"}
DB_CONNECTION = sqlite3.connect(
    (ROOT_PATH.parent / "pythonsqlite.db").as_posix(), check_same_thread=False
)

app = dash.Dash(
    __name__,
    title="Morlingue",
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
)
app.layout = html.Div(
    style={
        "backgroundColor": COLORS["background"],
        "height": "100vh",
        "width": "100%",
    },
    children=[
        html.H1(
            children="💰 Zamal's Morlingue 💰",
            style={"textAlign": "center", "color": COLORS["text"]},
        ),
        dcc.Interval(id="interval-component", interval=HOUR * 1000, n_intervals=0),
        html.Div(
            children="Assets summary in €",
            style={"textAlign": "center", "color": COLORS["text"]},
        ),
        dcc.Graph(id="kraken-graph"),
        html.Div(
            children="Sliding window",
            style={"textAlign": "center", "color": COLORS["text"]},
        ),
        dcc.Graph(id="sliding-graph"),
    ],
)


@app.callback(
    Output("kraken-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graph_live(n):
    df_assets = pd.read_sql_query("SELECT * FROM assets", DB_CONNECTION)
    df_assets["date"] = pd.to_datetime(df_assets["date"])
    df_assets = df_assets.drop(columns=["id"], axis=1)
    df_assets = df_assets.set_index("date")

    fig = px.line(height=800, labels={"y": "€", "x": ""})
    for crypto in df_assets.columns:
        fig.add_scatter(x=df_assets.index, y=df_assets[crypto], name=crypto)
    fig.update_layout(
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font_color=COLORS["text"],
    )
    fig.update_traces(marker=dict(color="cyan"))
    fig.update_xaxes(gridcolor=COLORS["line"])
    fig.update_yaxes(gridcolor=COLORS["line"])
    return fig


@app.callback(
    Output("sliding-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graph_live(n):
    df_assets = pd.read_sql_query("SELECT * FROM assets", DB_CONNECTION)
    df_assets["date"] = pd.to_datetime(df_assets["date"])
    df_assets = df_assets.drop(columns=["id"], axis=1)
    df_assets = df_assets.set_index("date")

    range_x = [
        (df_assets.index[-1] - pd.Timedelta(days=10)),
        df_assets.index[-1],
    ]
    fig = px.line(height=800, labels={"y": "€", "x": ""}, range_x=range_x)
    for crypto in df_assets.columns:
        fig.add_scatter(x=df_assets.index, y=df_assets[crypto], name=crypto)
    fig.update_layout(
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font_color=COLORS["text"],
    )
    fig.update_traces(marker=dict(color="cyan"))
    fig.update_xaxes(gridcolor=COLORS["line"])
    fig.update_yaxes(gridcolor=COLORS["line"])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")


# def _init_asset(
#         dataframe: pd.DataFrame,
#         name: str,
#         val: int,
#         start_date: pd.Timestamp,
#         kraken_val: int,
# ) -> pd.DataFrame:
#     dataframe[name] = 0
#     dataframe[name][dataframe["date"] > start_date] = val
#     # add rows "date-1" & "date" for viz
#     row = dataframe.iloc[-1, :].to_dict().copy()
#     row["kraken_total"] = kraken_val
#     row["date"] = start_date
#     row[name] = 0
#     dataframe = dataframe.append(row, ignore_index=True)
#     row["date"] = start_date + pd.DateOffset(1)
#     row[name] = val
#     dataframe = dataframe.append(row, ignore_index=True)
#     return dataframe
#
#
# def _init_df() -> pd.DataFrame:
#     # load from bdd
#     dataframe = pd.read_sql_query("SELECT * FROM assets", connect())
#     dataframe["date"] = pd.to_datetime(dataframe["date"])
#     dataframe = dataframe.drop(columns=["id"], axis=1)
#
#     # init values from the past
#     dataframe = dataframe.append(
#         {"date": pd.Timestamp(year=2016, month=9, day=1), "kraken_total": 500},
#         ignore_index=True,
#     )
#
#     # init static values
#     init_values = [
#         {
#             "name": "sax",
#             "val": 6000,
#             "start_date": pd.Timestamp(year=2018, month=9, day=1),
#             "kraken_val": 5000,
#         },
#         {
#             "name": "loan",
#             "val": 13000,
#             "start_date": pd.Timestamp(year=2019, month=4, day=1),
#             "kraken_val": 10000,
#         },
#         {
#             "name": "filly",
#             "val": 2100,
#             "start_date": pd.Timestamp(year=2020, month=7, day=1),
#             "kraken_val": 10000,
#         },
#         {
#             "name": "gold",
#             "val": 10000,
#             "start_date": pd.Timestamp(year=2020, month=9, day=1),
#             "kraken_val": 10000,
#         },
#         {
#             "name": "vieplus",
#             "val": 12000,
#             "start_date": pd.Timestamp(year=2020, month=11, day=1),
#             "kraken_val": 11000,
#         },
#         {
#             "name": "mg",
#             "val": 21000,
#             "start_date": pd.Timestamp(year=2020, month=12, day=20),
#             "kraken_val": 30000,
#         },
#     ]
#     for el in init_values:
#         dataframe = _init_asset(dataframe, **el)
#
#     return dataframe.sort_values(by=["date"])
#
# df = _init_df()
#
# kraken_total_df = df.set_index("date")["kraken_total"]
# kraken_total_df.name = "kraken ₿"
# fig = px.line(kraken_total_df, labels={"value": "€", "date": ""})
#
# # TODO: dynamic
# # df["metamask"] = 7959
# # fig.add_scatter(x=df["date"], y=df["metamask"], mode="lines", name="ETH Ξ")
# fig.add_scatter(x=df["date"], y=df["filly"], mode="lines", name="Filly 🐎")
# fig.add_scatter(x=df["date"], y=df["loan"], mode="lines", name="RB's loan 🏦")
# fig.add_scatter(x=df["date"], y=df["vieplus"], mode="lines", name="Vieplus 🏥")
# fig.add_scatter(x=df["date"], y=df["mg"], mode="lines", name="MG 🏎️")
# fig.add_scatter(x=df["date"], y=df["gold"], mode="lines", name="Gold 🥇")
# fig.add_scatter(x=df["date"], y=df["sax"], mode="lines", name="Sax 🎷")
# fig.add_scatter(x=df["date"], y=df.sum(axis=1), mode="lines", name="Total 💶")
# st.plotly_chart(fig)
#
# dataframe = pd.read_sql_query("SELECT * FROM crypto", connect())
# dataframe["date"] = pd.to_datetime(dataframe["date"])
# fig = px.line(x=dataframe["date"], y=dataframe["XXBT"], labels={"y": "€", "x": ""})
# fig.add_scatter(x=dataframe["date"], y=dataframe["XLTC"])
# fig.add_scatter(x=dataframe["date"], y=dataframe["XETH"])
# st.plotly_chart(fig)
