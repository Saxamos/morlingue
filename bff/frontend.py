import time
from datetime import datetime

import streamlit as st

from bff import ROOT_PATH
from bff.backend import fetch_youtube_data

st.set_page_config(
    page_title="Les BFF 💖", page_icon=(ROOT_PATH / "favicon.ico").as_posix()
)
st.title("Les BFF 💖")
st.markdown(f"Statistiques sur le compte youtube de *AD’OCC*")
name, statistics = fetch_youtube_data()
st.markdown(
    f"""
Nombre de vues total : **{statistics["viewCount"]}**

Nombre d'abonnés : **{statistics["subscriberCount"]}**

Nombre de vidéos : **{statistics["videoCount"]}**
"""
)
st.text(f"Dernière MAJ : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.image((ROOT_PATH / "shoshana.png").as_posix())

with st.empty():
    time.sleep(3600)
    st.experimental_rerun()

# TODO: add info https://developers.google.com/youtube/v3/docs/channels/list
# TODO: try dash for straeming
