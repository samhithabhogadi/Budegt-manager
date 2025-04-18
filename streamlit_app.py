import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime
import yfinance as yf
import hashlib
import re

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
    if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]).{6,}$", password):
        st.error("Password must include letters, numbers, and special characters and be at least 6 characters long.")
        st.stop()
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Load the CSV data
budget_data = load_data()

# ✅ Sidebar Navigation
st.sidebar.title("📊 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Add Entry", "Analysis", "Wealth Tracker", "Investment Suggestions", "Financial Education"])

# ✅ Username and Password Input
st.header("👤 User Login")
username = st.text_input("Enter your username", key="username")
password = st.text_input("Enter your password", type="password", key="password")

if not username or not password:
    st.warning("Please enter both username and password to continue.")
    st.stop()

hashed_password = hash_password(password)
user_data = budget_data[(budget_data['Username'] == username) & (budget_data['Password'] == hashed_password)]

if user_data.empty:
    if st.button("Register New User"):
        st.success("✅ New user registered. You can now start adding your data.")
        new_user = pd.DataFrame([[username, hashed_password, pd.NaT, 0, 0, "", "", "", None]],
                                columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
        budget_data = pd.concat([budget_data, new_user], ignore_index=True)
        save_data(budget_data)
        st.experimental_rerun()
    else:
        st.stop()

# ✅ Home Section
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
    user_data = budget_data[budget_data['Username'] == username]
    if not user_data.empty:
        latest_entry = user_data.sort_values("Date", ascending=False)
        st.dataframe(latest_entry)
    else:
        st.info("No data available. Please add entries.")

# ✅ Add Entry Section
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

# ✅ Analysis Section
elif section == "Analysis":
    st.title("📊 Financial Overview")
    student_data = budget_data[budget_data['Username'] == username]
    if not student_data.empty:
        total_income = student_data['Income'].sum()
        total_expenses = student_data['Expenses'].sum()
        total_savings = total_income - total_expenses

        st.metric("Total Income", f"₹{total_income:.2f}")
        st.metric("Total Expenses", f"₹{total_expenses:.2f}")
        st.metric("Estimated Savings", f"₹{total_savings:.2f}")

        st.subheader("📈 Income vs Expenses Over Time")
        line_data = student_data.sort_values("Date")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=line_data['Date'], y=line_data['Income'], mode='lines+markers', name='Income'))
        fig.add_trace(go.Scatter(x=line_data['Date'], y=line_data['Expenses'], mode='lines+markers', name='Expenses'))
        st.plotly_chart(fig)

        st.subheader("📊 Investment Plan with Current Prices")
        if student_data['Investment Plan'].str.contains("Stocks|Crypto").any():
            stocks = ["AAPL", "

