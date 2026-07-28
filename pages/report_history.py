import streamlit as st
import pandas as pd

from modules.database_functions import get_reports


def render_report_history():
    st.title("🗂️ Report History")
    st.caption("Review, edit, and re-export inspection reports.")
    reports = get_reports()
    if not reports:
        st.info("No reports have been generated yet")
        return

    report_options = [f"{report['report_id']} - {report['report_name']}" for report in reports]
    selected_report_index = st.selectbox("Choose a report", range(len(report_options)), format_func=lambda i: report_options[i])
    selected_report = reports[selected_report_index]

    st.markdown("**Selected Report**")
    st.write(f"**Report Name:** {selected_report['report_name']}")
    st.write(f"**Inspection ID:** {selected_report['inspection_id']}")
    st.write(f"**Created At:** {selected_report['created_at']}")

    if st.button("Edit Selected Report"):
        st.session_state.inspection_id = selected_report["inspection_id"]
        st.success("Report loaded for editing. Go to Generate Report to update and re-export.")

    if st.button("Download Selected Report"):
        with open(selected_report['pdf_path'], 'rb') as fh:
            st.download_button(
                label=f"Download {selected_report['report_name']}",
                data=fh.read(),
                file_name=selected_report['report_name'],
                mime='application/pdf',
            )

    st.markdown("---")
    st.subheader("Report History Table")
    df = pd.DataFrame(reports)
    st.dataframe(df)
