import streamlit as st
from datetime import date, datetime

from modules.database_functions import create_inspection, create_vehicle, get_vehicle
from utils import ensure_session, format_inspector_notes


def render_vehicle_information():
    st.title("🚗 Vehicle Information")
    st.caption("Capture the core vehicle and customer details required for the inspection report.")

    vehicle_id = st.session_state.get("vehicle_id")
    inspection_id = st.session_state.get("inspection_id")
    existing_vehicle = None
    if vehicle_id:
        existing_vehicle = get_vehicle(vehicle_id)

    if existing_vehicle and inspection_id:
        st.info(f"Continuing pending inspection #{inspection_id} for {existing_vehicle.get('make', '')} {existing_vehicle.get('model', '')}.")

    inspector_default = (
        existing_vehicle.get("inspector_name")
        if existing_vehicle
        else st.session_state.user.get("full_name", "") if st.session_state.get("user") else ""
    )
    inspection_date_default = (
        datetime.strptime(existing_vehicle["inspection_date"], "%Y-%m-%d").date()
        if existing_vehicle and existing_vehicle.get("inspection_date")
        else date.today()
    )

    with st.form("vehicle_info_form"):
        inspection_date = st.date_input("Inspection Date", value=inspection_date_default)
        make = st.text_input("Vehicle Make", value=existing_vehicle.get("make", "") if existing_vehicle else "")
        model = st.text_input("Vehicle Model", value=existing_vehicle.get("model", "") if existing_vehicle else "")
        year = st.text_input("Year", value=existing_vehicle.get("year", "") if existing_vehicle else "")
        vin = st.text_input("VIN", value=existing_vehicle.get("vin", "") if existing_vehicle else "")
        engine = st.text_input("Engine", value=existing_vehicle.get("engine", "") if existing_vehicle else "")
        odometer = st.text_input("Odometer Reading", value=existing_vehicle.get("odometer", "") if existing_vehicle else "")
        transmission = st.text_input("Transmission Type", value=existing_vehicle.get("transmission", "") if existing_vehicle else "")
        fuel_type = st.text_input("Fuel Type", value=existing_vehicle.get("fuel_type", "") if existing_vehicle else "")
        color = st.text_input("Color", value=existing_vehicle.get("color", "") if existing_vehicle else "")
        interior_type = st.text_input("Interior Type", value=existing_vehicle.get("interior_type", "") if existing_vehicle else "")
        spec = st.text_input("Regional Specifications / Spec", value=existing_vehicle.get("spec", "") if existing_vehicle else "")
        accident_history = st.text_input("Accident History", value=existing_vehicle.get("accident_history", "") if existing_vehicle else "")
        remarks = st.text_area("Remarks", value=existing_vehicle.get("remarks", "") if existing_vehicle else "")
        submitted = st.form_submit_button("Save Vehicle Information")

    if submitted:
        required_fields = [make, model, year, vin, engine, odometer, transmission, fuel_type, color, interior_type, spec, accident_history]
        if any(not field for field in required_fields):
            st.error("Please fill in the required fields before continuing.")
            return
        vehicle_data = {
            "make": make,
            "model": model,
            "year": year,
            "vin": vin,
            "engine": engine,
            "odometer": odometer,
            "transmission": transmission,
            "fuel_type": fuel_type,
            "color": color,
            "interior_type": interior_type,
            "spec": spec,
            "accident_history": accident_history,
            "remarks": remarks,
            "inspection_date": inspection_date.strftime("%Y-%m-%d"),
        }
        if existing_vehicle and vehicle_id:
            st.info("Vehicle already captured. Proceed to the next inspection page.")
        else:
            vehicle_id = create_vehicle(vehicle_data)
            st.session_state.vehicle_id = vehicle_id
            inspection_id = create_inspection(vehicle_id)
            st.session_state.inspection_id = inspection_id
            st.success("Vehicle information saved. You can now continue to the inspection sections.")