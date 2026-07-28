import streamlit as st

from modules.database_functions import delete_photo, get_photos, save_photo
from modules.image_handler import process_image_upload


def render_history_photos():
    st.title("🖼️ History Photos")
    st.caption("Add supporting historical photos and captions for the inspection record.")
    inspection_id = st.session_state.get("inspection_id")
    if not inspection_id:
        st.info("Start a new inspection first.")
        return
    caption = st.text_input("Photo caption")
    uploaded_files = st.file_uploader("Upload history photos", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
    if st.button("Save History Photos"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                saved_path = process_image_upload(uploaded_file, inspection_id, "History Photos", caption or "History Photo")
                if saved_path:
                    save_photo(inspection_id, "History Photos", saved_path, caption=caption or "History Photo")
            st.success("History photos saved")
        else:
            st.error("Please upload at least one image")

    st.markdown("---")
    photos = get_photos(inspection_id, category="History Photos")
    if photos:
        for photo in photos:
            cols = st.columns([3, 1])
            with cols[0]:
                st.image(photo["file_path"], caption=photo.get("caption", ""), width=220)
            with cols[1]:
                if st.button("Remove", key=f"delete_history_photo_{photo['photo_id']}"):
                    if delete_photo(photo["photo_id"]):
                        st.success("History photo removed successfully")
                        st.rerun()
                    else:
                        st.error("Unable to remove history photo.")
    else:
        st.info("No history photos yet")
