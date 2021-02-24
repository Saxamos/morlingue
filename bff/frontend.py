import streamlit as st

from bff import ROOT_PATH

st.set_page_config(
    page_title="Les BFF 💖", page_icon=(ROOT_PATH / "favicon.ico").as_posix()
)
st.write(
    """
# Web app des BFF 💖
"""
)

st.image((ROOT_PATH / "shoshana.png").as_posix())
