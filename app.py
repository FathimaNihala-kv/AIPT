import streamlit as st

from config import PAGE_ORDER
from database import initialize_database
from pages.body_shell import render_body_shell
from pages.brakes import render_brakes
from pages.chassis import render_chassis
from pages.coolant_system import render_coolant_system
from pages.dashboard import render_dashboard
from pages.diagnostic_scan import render_diagnostic_scan
from pages.engine import render_engine
from pages.exterior import render_exterior
from pages.generate_report import render_generate_report
from pages.glasses import render_glasses
from pages.history_photos import render_history_photos
from pages.inspection_summary import render_inspection_summary
from pages.interior import render_interior
from pages.other import render_other
from pages.paint_condition import render_paint_condition
from pages.report_history import render_report_history
from pages.suspension_steering import render_suspension_steering
from pages.transmission import render_transmission
from pages.tyres_wheels import render_tyres_wheels
from pages.undercarriage import render_undercarriage
from pages.vehicle_information import render_vehicle_information
from pages.vehicle_photos import render_vehicle_photos
from pages.ac import render_ac
from utils import ensure_session, load_css, render_sidebar


st.set_page_config(page_title="AutoInspect Pro", page_icon="🚗", layout="wide")
load_css()
ensure_session()
initialize_database()

redirect_page = st.session_state.get("redirect_page")
if redirect_page:
    st.session_state.sidebar_nav = redirect_page
    st.session_state.redirect_page = None

selected_page = render_sidebar(PAGE_ORDER)
if selected_page == "Dashboard":
    render_dashboard()
elif selected_page == "Vehicle Information":
    render_vehicle_information()
elif selected_page == "Vehicle Photos":
    render_vehicle_photos()
elif selected_page == "Body Shell":
    render_body_shell()
elif selected_page == "Chassis":
    render_chassis()
elif selected_page == "Paint Condition":
    render_paint_condition()
elif selected_page == "Exterior":
    render_exterior()
elif selected_page == "Glasses":
    render_glasses()
elif selected_page == "Tyres & Wheels":
    render_tyres_wheels()
elif selected_page == "Brakes":
    render_brakes()
elif selected_page == "Engine":
    render_engine()
elif selected_page == "Coolant System":
    render_coolant_system()
elif selected_page == "Transmission":
    render_transmission()
elif selected_page == "Suspension & Steering":
    render_suspension_steering()
elif selected_page == "Undercarriage":
    render_undercarriage()
elif selected_page == "Air Conditioning":
    render_ac()
elif selected_page == "Interior":
    render_interior()
elif selected_page == "History Photos":
    render_history_photos()
elif selected_page == "Diagnostic Scan":
    render_diagnostic_scan()
elif selected_page == "Other":
    render_other()
elif selected_page == "Inspection Summary":
    render_inspection_summary()
elif selected_page == "Generate Report":
    render_generate_report()
elif selected_page == "Report History":
    render_report_history()
