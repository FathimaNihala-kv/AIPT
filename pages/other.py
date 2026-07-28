import streamlit as st

from utils import render_inspection_page


def render_other():
    render_inspection_page(
        "Other",
        "Other",
        ["Additional Notes"],
        inspection_id=st.session_state.get("inspection_id"),
    )
