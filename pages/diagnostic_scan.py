import streamlit as st
from pathlib import Path

from config import UPLOADS_DIR
from modules.database_functions import get_photos, save_photo


def render_diagnostic_scan():
    st.title("🧪 Diagnostic Scan")
    st.caption("Upload the diagnostic scan PDF for this inspection.")
    inspection_id = st.session_state.get("inspection_id")
    if not inspection_id:
        st.info("Start a new inspection first.")
        return

    scan_pdf = st.file_uploader("Upload Scan PDF", type=["pdf"])

    if st.button("Save Diagnostic Scan"):
        if scan_pdf:
            safe_name = "".join(
                character for character in Path(scan_pdf.name).name
                if character.isalnum() or character in (".", "-", "_")
            )
            saved_path = UPLOADS_DIR / f"{inspection_id}_diagnostic_scan_{safe_name}"
            saved_path.write_bytes(scan_pdf.getbuffer())
            save_photo(inspection_id, "Diagnostic Scan", saved_path, caption="Scan PDF")
            st.success("Diagnostic scan PDF saved")
        else:
            st.warning("Please upload a diagnostic scan PDF first")

    st.markdown("---")
    st.subheader("Saved evidence")
    photos = get_photos(inspection_id, category="Diagnostic Scan")
    if photos:
        for photo in photos:
            file_path = Path(photo["file_path"])
            if file_path.suffix.lower() == ".pdf" and file_path.exists():
                st.download_button(
                    f"Download {photo.get('caption', file_path.name)}",
                    file_path.read_bytes(),
                    file_name=file_path.name,
                    mime="application/pdf",
                    key=f"download_scan_{photo['photo_id']}",
                )
            else:
                st.warning(f"Missing scan PDF: {file_path.name}")
    else:
        st.info("No diagnostic scan evidence yet")
