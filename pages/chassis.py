import streamlit as st

from utils import render_inspection_page


def render_chassis():
    render_inspection_page(
        "Chassis",
        "Chassis",
        ["Chassis"],
        inspection_id=st.session_state.get("inspection_id"),
    )
