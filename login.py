import bcrypt
import streamlit as st

from database import get_connection


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def ensure_admin_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", ("admin",))
    existing = cursor.fetchone()
    if not existing:
        cursor.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            ("admin", hash_password("admin123"), "System Administrator", "Administrator"),
        )
        cursor.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            ("inspector", hash_password("inspect123"), "Vehicle Inspector", "Inspector"),
        )
        conn.commit()
    conn.close()


def authenticate(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return None
    if verify_password(password, user["password"]):
        return dict(user)
    return None


def render_login():
    st.title("🚗 AutoInspect Pro")
    st.subheader("Premium Vehicle Inspection Report Management System")
    st.markdown("Login to manage inspections, generate reports, and track vehicle condition history.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        ensure_admin_user()
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"Welcome back, {user['full_name'] or user['username']}")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.markdown("---")
    st.caption("Default credentials: admin / admin123")


def render_change_password():
    st.subheader("Change Password")
    with st.form("change_password"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Update Password")
    if submitted:
        if new_password != confirm_password:
            st.error("Passwords do not match")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (st.session_state.user["username"],))
        row = cursor.fetchone()
        if not row or not verify_password(current_password, row["password"]):
            st.error("Current password is incorrect")
            conn.close()
            return
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hash_password(new_password), st.session_state.user["username"]))
        conn.commit()
        conn.close()
        st.success("Password updated successfully")


def render_forgot_password():
    st.subheader("Forgot Password")
    with st.form("forgot_password"):
        username = st.text_input("Username")
        submitted = st.form_submit_button("Reset Password")
    if submitted:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hash_password("AutoInspect2026!"), username))
            conn.commit()
            st.success("Password reset successfully. Please sign in with AutoInspect2026!")
        else:
            st.error("No account found for that username")
        conn.close()
