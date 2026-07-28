import streamlit as st

from modules.database_functions import (
    get_inspection,
    get_photos,
    get_vehicle,
    get_inspection_items,
    save_report,
    get_report_by_inspection,
    update_report,
    update_inspection_summary,
)
from modules.pdf_generator import create_report_pdf
from utils import format_inspector_notes


def render_generate_report():
    st.title("📄 Generate Report")
    st.caption("Create or edit a premium PDF report for the selected inspection.")
    inspection_id = st.session_state.get("inspection_id")
    if not inspection_id:
        st.info("Start a new inspection first or choose a report from Report History.")
        return

    inspection = get_inspection(inspection_id)
    vehicle = get_vehicle(inspection.get("vehicle_id"))
    items = get_inspection_items(inspection_id)
    photos = get_photos(inspection_id)
    reports = get_report_by_inspection(inspection_id)
    existing_report = reports[0] if reports else None

    report_name = st.text_input(
        "Report File Name",
        value=existing_report.get("report_name", f"Inspection_{inspection_id}.pdf") if existing_report else f"Inspection_{inspection_id}.pdf",
    )
    summary_notes = st.text_area(
        "Editable Summary Notes",
        value=format_inspector_notes(existing_report.get("report_notes", inspection.get("remarks", "")) if existing_report else inspection.get("remarks", "")),
        height=180,
        help="Press Enter for a new bullet point.",
    )

    if st.button("Generate PDF"):
        formatted_notes = format_inspector_notes(summary_notes)
        inspection["remarks"] = formatted_notes
        report_path = create_report_pdf(inspection_id, vehicle, inspection, items, photos)
        if existing_report:
            update_report(existing_report["report_id"], report_name, report_path, formatted_notes)
        else:
            save_report(inspection_id, report_name, report_path, formatted_notes)
        update_inspection_summary(
            inspection_id,
            score=0.0,
            status="Completed",
            completion=100.0,
            remarks=formatted_notes,
        )
        st.success(f"Report generated successfully at {report_path}")
        with open(report_path, "rb") as fh:
            st.download_button("Download PDF", fh.read(), file_name=report_name, mime="application/pdf")
