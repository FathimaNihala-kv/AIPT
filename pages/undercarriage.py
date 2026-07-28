import streamlit as st

from utils import render_inspection_page


def render_undercarriage():
    render_inspection_page(
        "Undercarriage",
        "Undercarriage",
        ["Undercarriage"],
        inspection_id=st.session_state.get("inspection_id"),
    )
