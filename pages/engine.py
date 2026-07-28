import streamlit as st

from utils import render_inspection_page


def render_engine():
    render_inspection_page(
        "Engine",
        "Engine",
        ["Engine"],
        inspection_id=st.session_state.get("inspection_id"),
    )
