import sqlite3

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from morlingue import HOUR, ROOT_PATH

COLORS = {
    "background": "lightslategray",
    "line": "darkslategray",
    "second_line": "#ffe476",
    "text": "lightcyan",
}
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
        dcc.Graph(id="total-graph"),
        html.Div(
            children="Sliding window",
            style={"textAlign": "center", "color": COLORS["text"]},
        ),
        dcc.Graph(id="sliding-graph"),
    ],
)


@app.callback(
    Output("total-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_total_graph_live(n):
    df_assets = pd.read_sql_query("SELECT * FROM assets", DB_CONNECTION)
    df_assets["date"] = pd.to_datetime(df_assets["date"])
    df_assets = df_assets.drop(columns=["id"], axis=1)
    df_assets = df_assets.set_index("date")

    fig = px.line(height=800, labels={"y": "€", "x": ""})
    total_sum = df_assets[["kraken_total", "metamask_total"]].sum(axis=1)
    fig.add_scatter(x=df_assets.index, y=total_sum, name="kraken_total")
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
def update_sliding_graph_live(n):
    df_assets = pd.read_sql_query("SELECT * FROM assets", DB_CONNECTION)
    df_assets["date"] = pd.to_datetime(df_assets["date"])
    df_assets = df_assets.drop(columns=["id"], axis=1)
    df_assets = df_assets.set_index("date")

    # filter by time
    df_assets = df_assets.loc[df_assets.index[-1] - pd.Timedelta(days=10) :, :]

    fig = px.line(height=800, labels={"y": "€", "x": ""})
    fig.add_scatter(x=df_assets.index, y=df_assets["kraken_total"], name="kraken_total")
    fig.add_scatter(
        x=df_assets.index,
        y=df_assets["metamask_total"],
        name="metamask_total",
        line_color=COLORS["second_line"],
    )
    fig.update_layout(
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font_color=COLORS["text"],
    )
    fig.update_traces(marker=dict(color="cyan"))
    fig.update_xaxes(gridcolor=COLORS["line"])
    fig.update_yaxes(gridcolor=COLORS["line"], rangemode="normal")
    return fig


def main():
    app.run_server(debug=True, host="0.0.0.0")
