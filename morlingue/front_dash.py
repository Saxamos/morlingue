import sqlite3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from morlingue import ROOT_PATH

# DB
db_path = (ROOT_PATH.parent / "pythonsqlite.db").as_posix()
connection = sqlite3.connect(db_path, check_same_thread=False)

# Colors
colors = {"background": "lightslategray", "line": "darkslategray", "text": "lightcyan"}

# Dataframe
df_assets = pd.read_sql_query("SELECT * FROM assets", connection)
df_assets["date"] = pd.to_datetime(df_assets["date"])
df_assets = df_assets.drop(columns=["id"], axis=1)
df_assets = df_assets.set_index("date")

df_crypto = pd.read_sql_query("SELECT * FROM crypto", connection)
df_crypto["date"] = pd.to_datetime(df_crypto["date"])
df_crypto = df_crypto.set_index("date")


# Plotly graph
def ploter(dataframe):
    fig = px.line(height=800, labels={"y": "€", "x": ""})
    for crypto in dataframe.columns:
        fig.add_scatter(x=dataframe.index, y=dataframe[crypto], name=crypto)
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
    fig.update_traces(marker=dict(color="cyan"))
    fig.update_xaxes(gridcolor=colors["line"])
    fig.update_yaxes(gridcolor=colors["line"])
    return fig


fig_asset = ploter(df_assets)
fig_crypto = ploter(df_crypto)

# Dash app
app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
app.layout = html.Div(
    style={
        "backgroundColor": colors["background"],
        "height": "100vh",
        "width": "100%",
    },
    children=[
        html.H1(
            children="💰 Zamal's Morlingue 💰",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            children="Assets summary in €",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Graph(id="all-graph", figure=fig_asset),
        html.Div(
            children="Crypto values in €",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Graph(id="crypto-graph", figure=fig_crypto),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
