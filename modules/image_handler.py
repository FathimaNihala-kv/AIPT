import os
import uuid
from pathlib import Path

from PIL import Image
import streamlit as st

from config import UPLOADS_DIR


def process_image_upload(uploaded_file, inspection_id, category, part_name):
    try:
        image = Image.open(uploaded_file)
        image = image.convert("RGB")
        safe_name = f"{inspection_id}_{category}_{part_name}_{uuid.uuid4().hex[:8]}".replace(" ", "_")
        output_path = UPLOADS_DIR / f"{safe_name}.jpg"
        image.save(output_path, optimize=True, quality=80)
        return output_path
    except Exception as exc:
        st.error(f"Image could not be processed: {exc}")
        return None
