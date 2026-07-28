import streamlit as st

from utils import render_inspection_page


def render_brakes():
    render_inspection_page(
        "Brakes",
        "Brakes",
        ["Brakes"],
        inspection_id=st.session_state.get("inspection_id"),
    )
