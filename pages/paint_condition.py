import streamlit as st

from utils import render_inspection_page


def render_paint_condition():
    render_inspection_page(
        "Paint Condition",
        "Paint Condition",
        ["Paint Condition"],
        inspection_id=st.session_state.get("inspection_id"),
    )
