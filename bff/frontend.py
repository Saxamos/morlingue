import time
from datetime import datetime

import plotly_express as px
import streamlit as st

from bff import ROOT_PATH
from bff.backend import fetch_youtube_data

st.set_page_config(
    page_title="Les BFF 💖", page_icon=(ROOT_PATH / "favicon.ico").as_posix()
)
st.title("Les BFF 💖")
st.markdown("Statistiques de la playlist *cité de l'éco*")

dataframe = fetch_youtube_data()
fig = px.scatter(dataframe, x=dataframe.index, y="views", hover_name="title")
st.plotly_chart(fig)

st.dataframe(dataframe)

st.text(f"Dernière MAJ : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.image((ROOT_PATH / "shoshana.png").as_posix())

with st.empty():
    time.sleep(3600)
    st.experimental_rerun()

# TODO: try dash for streaming
