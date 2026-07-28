import streamlit as st

from utils import render_inspection_page


def render_transmission():
    render_inspection_page(
        "Transmission",
        "Transmission",
        ["Transmission"],
        inspection_id=st.session_state.get("inspection_id"),
    )
