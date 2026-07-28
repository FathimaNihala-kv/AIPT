import streamlit as st

from utils import render_inspection_page


def render_body_shell():
    render_inspection_page(
        "Body Shell",
        "Body Shell",
        ["Body Shell"],
        inspection_id=st.session_state.get("inspection_id"),
    )
