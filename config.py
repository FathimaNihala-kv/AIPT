from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"
DATABASE_PATH = DATABASE_DIR / "vehicle_inspection.db"
STYLES_PATH = ASSETS_DIR / "styles.css"

for path in [DATABASE_DIR, UPLOADS_DIR, REPORTS_DIR, ASSETS_DIR]:
    path.mkdir(exist_ok=True)

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

PAGE_ORDER = [
    "Dashboard",
    "Vehicle Information",
    "Vehicle Photos",
    "Body Shell",
    "Chassis",
    "Paint Condition",
    "Exterior",
    "Glasses",
    "Tyres & Wheels",
    "Brakes",
    "Engine",
    "Coolant System",
    "Transmission",
    "Suspension & Steering",
    "Undercarriage",
    "Air Conditioning",
    "Interior",
    "History Photos",
    "Diagnostic Scan",
    "Other",
    "Inspection Summary",
    "Generate Report",
    "Report History",
]

CONDITION_OPTIONS = ["Excellent", "Good", "Fair", "Poor", "Damaged", "Needs Replacement", "Not Inspected"]
SEVERITY_OPTIONS = ["None", "Minor", "Moderate", "Major", "Critical"]
