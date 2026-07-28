import streamlit as st

from utils import render_inspection_page


def render_ac():
    render_inspection_page(
        "Air Conditioning",
        "Air Conditioning",
        ["Air Conditioning"],
        inspection_id=st.session_state.get("inspection_id"),
    )
