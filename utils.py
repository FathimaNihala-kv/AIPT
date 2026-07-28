import os
import json
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st
from modules.database_functions import (
    save_inspection_item,
    get_inspection_items,
    delete_inspection_item,
    save_photo,
    get_photos,
)
from modules.image_handler import process_image_upload


def load_css():
    from config import STYLES_PATH

    if STYLES_PATH.exists():
        with open(STYLES_PATH, "r", encoding="utf-8") as fh:
            st.markdown(f"<style>{fh.read()}</style>", unsafe_allow_html=True)


def ensure_session():
    defaults = {
        "inspection_id": None,
        "vehicle_id": None,
        "sidebar_nav": "Dashboard",
        "redirect_page": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_inspection_session():
    st.session_state.inspection_id = None
    st.session_state.vehicle_id = None


def render_sidebar(navigation_items):
    from pathlib import Path

    logo_path = Path(__file__).resolve().parent / "assets" / "logo.png"
    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)
    else:
        st.sidebar.markdown("### 🚗 AutoInspect Pro")
    st.sidebar.title("AutoInspect Pro")
    st.sidebar.caption("Premium Vehicle Inspection Platform")
    selected = st.sidebar.radio("Navigation", navigation_items, key="sidebar_nav")
    st.sidebar.markdown("---")
    st.sidebar.button("New Inspection", on_click=reset_inspection_session)
    return selected


def format_inspector_notes(notes):
    if notes is None:
        return ""

    text = str(notes).strip()
    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    bullet_lines = []
    for line in lines:
        if line.startswith("- "):
            bullet_lines.append(line)
        elif line.startswith("• "):
            bullet_lines.append(f"- {line[2:].strip()}")
        else:
            bullet_lines.append(f"- {line}")
    return "\n".join(bullet_lines)


def render_inspection_page(page_title, category, parts, inspection_id=None, include_photo_uploader=True):
    if not inspection_id:
        st.info("Start a new inspection from the Vehicle Information page first.")
        return

    st.header(page_title)
    st.caption("Capture remarks and supporting images for each item.")

    for part in parts:
        with st.expander(part, expanded=True):
            col1, col2 = st.columns([1, 1])
            remarks = st.text_area("Remarks", key=f"{category}_{part}_remarks")
            uploaded_files = st.file_uploader(
                f"Upload photos for {part}",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key=f"{category}_{part}_upload",
            )
            if uploaded_files:
                st.markdown("**Preview selected images:**")
                preview_cols = st.columns(4)
                for index, uploaded_file in enumerate(uploaded_files):
                    preview_cols[index % 4].image(uploaded_file, width=160)
            if st.button(f"Save {part}", key=f"save_{category}_{part}"):
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        saved_path = process_image_upload(uploaded_file, inspection_id, category, part)
                        if saved_path:
                            save_photo(inspection_id, category, saved_path, caption=part)
                save_inspection_item(
                    inspection_id=inspection_id,
                    category=category,
                    part_name=part,
                    condition="",
                    severity="",
                    remarks=remarks,
                )
                st.success(f"{part} saved successfully.")

    st.markdown("---")
    st.subheader("Saved findings")
    items = get_inspection_items(inspection_id, category=category)
    if items:
        for item in items:
            cols = st.columns([5, 1])
            with cols[0]:
                st.write(f"- {item['part_name']} | Remarks: {item.get('remarks', '')}")
            with cols[1]:
                if st.button("Delete", key=f"delete_finding_{item['item_id']}"):
                    if delete_inspection_item(item["item_id"]):
                        st.success("Finding deleted.")
                        st.rerun()
                    else:
                        st.error("Unable to delete finding.")
    else:
        st.info("No findings saved for this section yet.")


def get_dashboard_metrics():
    from modules.database_functions import get_inspection_summary_counts

    return get_inspection_summary_counts()
