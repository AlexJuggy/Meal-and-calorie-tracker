import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Meal Tracker", page_icon="🥗", layout="wide")
st.title("🥗 Personal Meal & Calorie Tracker")

# -------------------------------------------------------------
# 1. SIDEBAR: Select User & Daily Summary
# -------------------------------------------------------------
st.sidebar.header("User Selection")

# Fetch all users from backend
try:
    users_resp = requests.get(f"{BACKEND_URL}/users/")
    users = users_resp.json() if users_resp.status_code == 200 else []
except Exception:
    st.sidebar.error("Could not connect to FastAPI backend. Is it running?")
    users = []

if users:
    user_options = {u["name"]: u["id"] for u in users}
    selected_user = st.sidebar.selectbox("Choose active user:", options = users, format_func=lambda u: f"{u['name']} (ID: {u['id']})")
    selected_user_name = selected_user["name"]
    selected_user_id = selected_user["id"]

    # Fetch User Details (Goal) & Summary
    user_data = requests.get(f"{BACKEND_URL}/users/{selected_user_id}").json()
    filter_date = st.sidebar.date_input("Select date:")
    summary_data = requests.get(f"{BACKEND_URL}/users/{selected_user_id}/summary", params={"target_date": str(filter_date)}).json()
    
    total_cals = summary_data.get("total_calories", 0)
    goal = user_data.get("calorie_goal", 2000)

    st.sidebar.divider()
    st.sidebar.metric("Total Calories Consumed", f"{total_cals} kcal")
    st.sidebar.metric("Target Goal", f"{goal} kcal")
    
    progress = min(total_cals / goal, 1.0) if goal > 0 else 0.0
    st.sidebar.progress(progress)
else:
    st.sidebar.info("No users found. Create one on the right!")
    selected_user_id = None

# -------------------------------------------------------------
# 2. MAIN PAGE: Create User & Log Meals
# -------------------------------------------------------------
col1, col2 = st.columns([1, 1])

# Column 1: Add New User
with col1:
    st.subheader("👤 Create New User")
    with st.form("new_user_form"):
        new_name = st.text_input("Name")
        new_goal = st.number_input("Daily Calorie Goal", min_value=500, max_value=10000, value=2000, step=50)
        submit_user = st.form_submit_button("Register User")
        
        if submit_user and new_name:
            payload = {"name": new_name, "daily_goal": int(new_goal)}
            res = requests.post(f"{BACKEND_URL}/users/", json=payload)
            if res.status_code in (200, 201):
                st.toast(f"User '{new_name}' added!")
                st.rerun()
            else:
                st.error(f"Failed ({res.status_code}): {res.text}")

# Column 2: Log Meal (if user selected)
with col2:
    st.subheader("🍽️ Log a Meal")
    if selected_user_id:
        with st.form("meal_form"):
            meal_name = st.text_input("Meal Description (e.g. Oatmeal, Chicken Salad)")
            calories = st.number_input("Calories", min_value=1, max_value=5000, value=400, step=10)
            logged_date = st.date_input("Date", value=date.today())
            submit_meal = st.form_submit_button("Log Meal")

            if submit_meal and meal_name:
                payload = {
                    "user_id": selected_user_id,
                    "name": meal_name,
                    "calories": int(calories),
                    "logged_in": str(logged_date)
                }
                res = requests.post(f"{BACKEND_URL}/meals/", json=payload)
                if res.status_code in (200, 201):
                    st.toast("Meal logged successfully!")
                    st.rerun()
                else:
                    st.error("Failed to record meal.")
    else:
        st.warning("Please create or select a user first.")

# -------------------------------------------------------------
# 3. MEAL HISTORY TABLE
# -------------------------------------------------------------
st.divider()
st.subheader("📋 Meal History for Selected Day")

if selected_user_id:
    meals_resp = requests.get(f"{BACKEND_URL}/meals/{selected_user_id}/{filter_date}")

    if meals_resp.status_code == 200:
        meals_list = meals_resp.json()
        if meals_list and isinstance(meals_list, list):
            # Display clean data table
            table_data = [{"Meal": m["name"], "Calories": f"{m['calories']} kcal", "Date": m["logged_in"]} for m in meals_list]
            st.table(table_data)
        else:
            st.info("No meals recorded for this date.")
    else:
        st.info("No meals found for this date.")