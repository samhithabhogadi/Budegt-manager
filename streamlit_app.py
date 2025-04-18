import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime
import hashlib

st.set_page_config(page_title="Student Wealth & Investment Hub", layout="wide", page_icon="💰")

# ✅ Load Data Function
@st.cache_data
def load_data():
    expected_columns = [
        "Username", "Password", "Date", "Monthly Income", "Monthly Expenses",
        "Daily Expenses", "Saving Goals", "Risk Appetite", "Investment Plan",
        "Age", "Expense Category", "Amount (₹)"
    ]
    try:
        df = pd.read_csv("student_budget_data.csv", parse_dates=['Date'])
        if not all(col in df.columns for col in expected_columns):
            raise ValueError("Missing columns")
    except (FileNotFoundError, ValueError):
        df = pd.DataFrame(columns=expected_columns)
        df.to_csv("student_budget_data.csv", index=False)
    return df

# ✅ Save Data Function
def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

# ✅ Hashing Function for Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Load the CSV data
budget_data = load_data()

# Session setup
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.hashed_password = ""

# User login and registration
if not st.session_state.authenticated:
    st.header("👤 User Login or Register")
    username = st.text_input("Enter your username", key="username_input")
    password = st.text_input("Enter your password", type="password", key="password_input")

    if username and password:
        hashed_password = hash_password(password)
        user_data = budget_data[(budget_data['Username'] == username) & (budget_data['Password'] == hashed_password)]

        if not user_data.empty:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.hashed_password = hashed_password
            st.success("✅ Logged in successfully!")

    if st.button("Register New User"):
        if username and password:
            hashed_password = hash_password(password)
            if username not in budget_data['Username'].values:
                new_user = pd.DataFrame([[username, hashed_password, None, 0.0, 0.0, 0.0, "", "", "", None, "", 0.0]],
                                         columns=["Username", "Password", "Date", "Monthly Income", "Monthly Expenses",
                                                  "Daily Expenses", "Saving Goals", "Risk Appetite", "Investment Plan",
                                                  "Age", "Expense Category", "Amount (₹)"])
                budget_data = pd.concat([budget_data, new_user], ignore_index=True)
                save_data(budget_data)
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.hashed_password = hashed_password
                st.success("✅ New user registered.")
else:
    username = st.session_state.username
    hashed_password = st.session_state.hashed_password
    user_data = budget_data[(budget_data['Username'] == username) & (budget_data['Password'] == hashed_password)]

    # Sidebar Navigation
    st.sidebar.title("📚 Student Financial Toolkit")
    section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Wealth Tracker", "Investment Suggestions", "Financial Education"])

    # Home Section
    if section == "Home":
        st.title("🎓 Welcome to the Student Wealth & Investment Hub")
        st.markdown(f"""
        Hello **{username}**, welcome back!

        Use this app to:
        - Track **monthly income**
        - Log **daily expenses** with categories
        - Set **saving goals**
        - Monitor your **investment preferences**
        - Visualize financial trends

        Your financial journey starts here! 🚀
        """)

    # Add Entry Section
    elif section == "Add Entry":
        st.title("➕ Add Financial Entry")

        with st.form("entry_form"):
            st.subheader("📅 Financial Details")
            age = st.number_input("Age", min_value=5, max_value=25)
            date = st.date_input("Date", value=datetime.today())
            income = st.number_input("Monthly Income (₹)", min_value=0.0, format="%.2f")
            monthly_expenses = st.number_input("Total Monthly Expenses (₹)", min_value=0.0, format="%.2f")
            daily_expenses = st.number_input("Total Daily Expenses (₹)", min_value=0.0, format="%.2f")
            saving_goals = st.text_input("Saving Goals")
            risk_appetite = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"])
            investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"])
            expense_category = st.text_input("Main Expense Category")
            amount = st.number_input("Main Expense Amount (₹)", min_value=0.0, format="%.2f")
            add_more = st.checkbox("Add more expense entries")
            submit = st.form_submit_button("Add Entry")

        if submit:
            new_row = pd.DataFrame([[username, hashed_password, date, income, monthly_expenses, daily_expenses, saving_goals, risk_appetite, investment_plan, age, expense_category, amount]],
                                   columns=["Username", "Password", "Date", "Monthly Income", "Monthly Expenses", "Daily Expenses",
                                            "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Expense Category", "Amount (₹)"])
            budget_data = pd.concat([budget_data, new_row], ignore_index=True)
            save_data(budget_data)

        if add_more:
            st.subheader("➕ Additional Expense Entries")
            default_expense_df = pd.DataFrame([{"Expense Category": "", "Amount (₹)": 0.0}])
            more_expenses = st.data_editor(default_expense_df, num_rows="dynamic", key="more_expenses_editor")

            if not more_expenses.empty:
                for _, row in more_expenses.iterrows():
                    try:
                        extra_expense = float(row["Amount (₹)"])
                        extra_category = row["Expense Category"]
                        if extra_expense > 0:
                            new_extra_row = pd.DataFrame([[username, hashed_password, datetime.today(), 0.0, 0.0, 0.0, "", "", "", age, extra_category, extra_expense]],
                                                         columns=["Username", "Password", "Date", "Monthly Income", "Monthly Expenses", "Daily Expenses",
                                                                  "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Expense Category", "Amount (₹)"])
                            budget_data = pd.concat([budget_data, new_extra_row], ignore_index=True)
                    except Exception:
                        continue
                save_data(budget_data)
                st.success("✅ Additional entries saved!")

    # Wealth Tracker Section (formerly Analysis)
    elif section == "Wealth Tracker":
        st.title("💼 Wealth Tracker")
        st.subheader("💸 Expenses & Remaining Wealth Overview")

        user_data = budget_data[(budget_data['Username'] == username)]

        if user_data.empty:
            st.warning("No data found. Please add entries first.")
        else:
            total_income = user_data['Monthly Income'].sum()
            total_expense = user_data['Amount (₹)'].sum() + user_data['Monthly Expenses'].sum() + user_data['Daily Expenses'].sum()
            total_savings = total_income - total_expense

            st.metric("💰 Total Income", f"₹{total_income:,.2f}")
            st.metric("📈 Total Expenses", f"₹{total_expense:,.2f}")
            st.metric("💵 Total Savings", f"₹{total_savings:,.2f}")

            # Pie Chart for Expense Distribution
            expense_df = user_data.groupby("Expense Category")["Amount (₹)"].sum().reset_index()
            if not expense_df.empty:
                fig = go.Figure(data=[go.Pie(labels=expense_df['Expense Category'], values=expense_df['Amount (₹)'], hole=.3)])
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("📊 Suggested Investment Strategy")
            if total_savings <= 0:
                st.info("No savings to invest yet. Try reducing expenses.")
            else:
                if total_savings < 1000:
                    st.write("Consider starting with a **Piggy Bank** or basic **Savings Account**.")
                elif total_savings < 5000:
                    st.write("Look into **Recurring Deposits** or **Low-risk Mutual Funds**.")
                elif total_savings < 15000:
                    st.write("Explore **Balanced Mutual Funds** or **Fixed Deposits**.")
                elif total_savings < 30000:
                    st.write("You can try **Index Funds** or **Conservative Stock Portfolios**.")
                else:
                    st.write("Consider **Stock Market**, **ETFs**, or even **Crypto** (based on your risk appetite).")
