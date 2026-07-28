import streamlit as st
import pandas as pd

from modules.database_functions import get_inspection_summary_counts, get_pending_inspections, search_inspections
from utils import get_dashboard_metrics


def render_dashboard():
    st.title("📊 Dashboard")
    st.caption("Monitor inspections, track pending reports, and manage the workflow in one place.")

    metrics = get_dashboard_metrics()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Inspections", metrics.get("total", 0))
    col2.metric("Today's Inspections", metrics.get("today", 0))
    col3.metric("Pending Reports", metrics.get("pending", 0))
    col4.metric("Completed Reports", metrics.get("completed", 0))

    st.markdown("---")
    st.subheader("Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)

    def redirect_to(page_name):
        st.session_state.redirect_page = page_name
        st.rerun()

    with action_col1:
        if st.button("Create New Inspection"):
            redirect_to("Vehicle Information")
    with action_col2:
        if st.button("View Report History"):
            redirect_to("Report History")
    with action_col3:
        if st.button("Generate Report"):
            redirect_to("Generate Report")

    st.markdown("---")
    st.subheader("Continue Pending Inspection")
    pending_inspections = get_pending_inspections()
    if pending_inspections:
        pending_options = [
            f"{item['inspection_id']} — {item['customer_name']} ({item['vin']})"
            for item in pending_inspections
        ]
        selected_index = st.selectbox("Select a pending inspection", range(len(pending_options)), format_func=lambda i: pending_options[i])
        if st.button("Continue Selected Inspection"):
            selected = pending_inspections[selected_index]
            st.session_state.inspection_id = selected["inspection_id"]
            st.session_state.vehicle_id = selected["vehicle_id"]
            redirect_to("Vehicle Information")
            st.success("Pending inspection loaded. You can continue from the Vehicle Information page or choose another section from the sidebar.")
    else:
        st.info("No pending inspections available. Start a new inspection to continue later.")

    st.markdown("---")
    query = st.text_input("Search by VIN, Registration, Customer Name, or Inspection ID")
    if query:
        results = search_inspections(query)
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.info("No matching inspections found")

    st.markdown("---")
    st.subheader("Recent Activity")
    st.info("Inspection workflow is ready. Start a new inspection from the sidebar to begin capturing data.")
