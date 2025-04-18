import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime
import yfinance as yf
import hashlib

st.set_page_config(page_title="Student Wealth & Investment Hub", layout="wide", page_icon="💰")

# ✅ Load Data Function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("student_budget_data.csv", parse_dates=['Date'])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
        df.to_csv("student_budget_data.csv", index=False)
    return df

# ✅ Save Data Function
def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

# ✅ Hashing Function for Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Load CSV data and ensure columns
budget_data = load_data()
required_columns = {"Username", "Password"}
if not required_columns.issubset(budget_data.columns):
    st.error("Data file is missing necessary columns. Please delete or fix the CSV file.")
    st.stop()

# ✅ Login Section
st.header("👤 User Login")
username = st.text_input("Enter your username", key="username")
password = st.text_input("Enter your password", type="password", key="password")

if not username or not password:
    st.warning("Please enter both username and password to continue.")
    st.stop()

hashed_password = hash_password(password)

# ✅ User Filtering
user_data = budget_data[(budget_data['Username'] == username) & (budget_data['Password'] == hashed_password)]

# ✅ Register if new
if user_data.empty and st.button("Register New User"):
    new_user = pd.DataFrame([[username, hashed_password, None, 0.0, 0.0, "", "", "", None]],
                             columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
    budget_data = pd.concat([budget_data, new_user], ignore_index=True)
    save_data(budget_data)
    st.success("✅ New user registered. You can now start adding your data.")

# Sidebar Navigation
st.sidebar.title("📚 Student Financial Toolkit")
section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Analysis", "Wealth Tracker", "Investment Suggestions", "Financial Education"])

# Home Section
if section == "Home":
    st.title("🎓 Welcome to the Student Wealth & Investment Hub")
    st.markdown("""
    Track your **income**, monitor your **expenses**, set **savings goals**, and explore **investment opportunities** based on your age and risk appetite.

    #### Features:
    - Add daily income & expense entries
    - View savings and financial analysis
    - Net worth tracking
    - Personalized investment advice
    """)

    st.subheader("📁 Your Budget Data")
    if not user_data.empty:
        latest_entry = user_data.sort_values("Date", ascending=False)
        st.dataframe(latest_entry)
    else:
        st.info("No data available. Please add entries.")

# Add Entry Section
elif section == "Add Entry":
    st.title("➕ Add Daily Financial Entry")
    num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=15, step=1)

    for i in range(int(num_entries)):
        st.markdown(f"### Entry {i+1}")
        with st.form(f"entry_form_{i}", clear_on_submit=True):
            if i == 0:
                age = st.number_input("Age", min_value=5, max_value=35, key=f"age_{i}")
                date = st.date_input("Date", value=datetime.today(), key=f"date_{i}")
                income = st.number_input("Daily Income (₹)", min_value=0.0, format="%.2f", key=f"income_{i}")
                expenses = st.number_input("Total Daily Expenses (₹)", min_value=0.0, format="%.2f", key=f"expenses_{i}")
                saving_goals = st.text_input("Saving Goals", key=f"savings_{i}")
                risk_appetite = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"], key=f"risk_{i}")
                investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"], key=f"plan_{i}")
            else:
                age = None
                income = 0.0
                saving_goals = ""
                risk_appetite = ""
                investment_plan = ""
                date = st.date_input("Date", value=datetime.today(), key=f"date_{i}")
                expenses = st.number_input("Total Daily Expenses (₹)", min_value=0.0, format="%.2f", key=f"expenses_{i}")
            submit = st.form_submit_button("Add Entry")

            if submit:
                new_row = pd.DataFrame([[username, hashed_password, date, income, expenses, saving_goals, risk_appetite, investment_plan, age]],
                                       columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
                budget_data = pd.concat([budget_data, new_row], ignore_index=True)
                save_data(budget_data)
                st.success(f"✅ Entry {i+1} added successfully!")
