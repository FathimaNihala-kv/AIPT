import streamlit as st

from utils import render_inspection_page


def render_interior():
    render_inspection_page(
        "Interior",
        "Interior",
        ["Interior"],
        inspection_id=st.session_state.get("inspection_id"),
    )
