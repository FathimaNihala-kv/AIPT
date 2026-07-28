import sqlite3
from pathlib import Path

from config import DATABASE_PATH


def get_connection():
    # Use a longer timeout to wait for locks to clear and enable WAL journal mode
    conn = sqlite3.connect(str(DATABASE_PATH), timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        # WAL reduces contention between readers and writers
        conn.execute("PRAGMA journal_mode=WAL;")
        # Balance durability vs performance
        conn.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        # If pragmas fail for any reason, continue with the connection
        pass
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            role TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            year TEXT,
            vin TEXT UNIQUE,
            engine TEXT,
            odometer TEXT,
            transmission TEXT,
            fuel_type TEXT,
            color TEXT,
            interior_type TEXT,
            spec TEXT,
            accident_history TEXT,
            registration_number TEXT,
            engine_number TEXT,
            origin_of_vehicle TEXT,
            vehicle_category TEXT,
            remarks TEXT,
            inspection_date TEXT,
            inspector_name TEXT,
            customer_name TEXT,
            customer_contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inspections (
            inspection_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            inspector_name TEXT,
            overall_score REAL DEFAULT 0,
            overall_status TEXT DEFAULT 'Pending',
            completion_percentage REAL DEFAULT 0,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inspection_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_id INTEGER,
            category TEXT,
            part_name TEXT,
            condition TEXT,
            severity TEXT,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(inspection_id) REFERENCES inspections(inspection_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_id INTEGER,
            category TEXT,
            file_path TEXT,
            caption TEXT,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(inspection_id) REFERENCES inspections(inspection_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_id INTEGER,
            report_name TEXT,
            pdf_path TEXT,
            report_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(inspection_id) REFERENCES inspections(inspection_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS report_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_id INTEGER,
            action TEXT,
            performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(inspection_id) REFERENCES inspections(inspection_id)
        )
        """
    )

    conn.commit()
    conn.close()


def migrate_vehicle_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(vehicles)")
    columns = [row[1] for row in cursor.fetchall()]
    if "spec" not in columns:
        cursor.execute("ALTER TABLE vehicles ADD COLUMN spec TEXT")
    conn.commit()
    conn.close()


def migrate_reports_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(reports)")
    columns = [row[1] for row in cursor.fetchall()]
    if "report_notes" not in columns:
        cursor.execute("ALTER TABLE reports ADD COLUMN report_notes TEXT")
    conn.commit()
    conn.close()


def migrate_photos_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(photos)")
    columns = [row[1] for row in cursor.fetchall()]
    if "remarks" not in columns:
        cursor.execute("ALTER TABLE photos ADD COLUMN remarks TEXT")
    conn.commit()
    conn.close()


def initialize_database():
    create_tables()
    migrate_vehicle_table()
    migrate_reports_table()
    migrate_photos_table()
