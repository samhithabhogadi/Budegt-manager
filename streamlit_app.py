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
    expected_columns = ["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"]
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
                new_user = pd.DataFrame([[username, hashed_password, None, 0.0, 0.0, "", "", "", None]],
                                         columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
                budget_data = pd.concat([budget_data, new_user], ignore_index=True)
                save_data(budget_data)
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.hashed_password = hashed_password
                st.success("✅ New user registered.")
            else:
                st.error("❌ Username already exists.")
else:
    username = st.session_state.username
    hashed_password = st.session_state.hashed_password
    user_data = budget_data[(budget_data['Username'] == username) & (budget_data['Password'] == hashed_password)]

    # Sidebar Navigation
    st.sidebar.title("📚 Student Financial Toolkit")
    section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Analysis", "Wealth Tracker", "Investment Suggestions", "Financial Education", "Logout"])

    # Logout
    if section == "Logout":
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.hashed_password = ""
        st.experimental_rerun()

    # Home Section
    elif section == "Home":
        st.title("🎓 Welcome to the Student Wealth & Investment Hub")
        st.markdown(f"""
        Hello **{username}**, welcome back!

        Use this app to:
        - Track **daily expenses** and **monthly income**
        - Set **saving goals**
        - Monitor your **investment preferences**
        - Visualize financial trends

        Your financial journey starts here! 🚀
        """)

    # Add Entry Section
    elif section == "Add Entry":
        st.title("➕ Add Financial Entry")
        with st.form("entry_form"):
            age = st.number_input("Age", min_value=5, max_value=35, step=1)
            date = st.date_input("Date", value=datetime.today())
            income = st.number_input("Monthly Income (₹)", min_value=0.0, format="%.2f")
            expenses = st.number_input("Daily Expense (₹)", min_value=0.0, format="%.2f")
            saving_goals = st.text_input("Saving Goals")
            risk_appetite = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"])
            investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"])
            submit = st.form_submit_button("Add Entry")

            if submit:
                new_row = pd.DataFrame([[username, hashed_password, date, income, expenses, saving_goals, risk_appetite, investment_plan, age]],
                                       columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
                budget_data = pd.concat([budget_data, new_row], ignore_index=True)
                save_data(budget_data)
                st.success("✅ Entry added successfully!")

    # Analysis Section
    elif section == "Analysis":
        st.title("📊 Financial Overview")
        if not user_data.empty:
            total_income = user_data['Income'].sum()
            total_expenses = user_data['Expenses'].sum()
            total_savings = total_income - total_expenses

            st.metric("Total Income (₹)", f"₹{total_income:.2f}")
            st.metric("Total Expenses (₹)", f"₹{total_expenses:.2f}")
            st.metric("Estimated Savings (₹)", f"₹{total_savings:.2f}")

            st.subheader("📈 Income vs Expenses Over Time")
            line_data = user_data.dropna().sort_values("Date")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=line_data['Date'], y=line_data['Income'], mode='lines+markers', name='Income'))
            fig.add_trace(go.Scatter(x=line_data['Date'], y=line_data['Expenses'], mode='lines+markers', name='Expenses'))
            st.plotly_chart(fig)

            st.subheader("💡 Smart Insights")
            if total_income > 0:
                savings_rate = (total_savings / total_income) * 100
                st.info(f"💸 You are saving {savings_rate:.2f}% of your income.")

                if savings_rate < 10:
                    st.warning("Consider reducing expenses or increasing income. Try creating a monthly budget.")
                elif savings_rate < 30:
                    st.info("You're doing okay! You might consider SIPs or hybrid mutual funds.")
                else:
                    st.success("Excellent saving rate! You could explore higher-yield investments like stocks or NPS.")
            else:
                st.info("Please add income to get insights.")
        else:
            st.info("No data available yet.")

    # Wealth Tracker Section
    elif section == "Wealth Tracker":
        st.title("💼 Expense vs Remaining Wealth")
        if not user_data.empty:
            total_income = user_data['Income'].sum()
            total_expenses = user_data['Expenses'].sum()
            remaining = total_income - total_expenses

            st.metric("Total Income (₹)", f"₹{total_income:.2f}")
            st.metric("Total Expenses (₹)", f"₹{total_expenses:.2f}")
            st.metric("Remaining Wealth (₹)", f"₹{remaining:.2f}")

            if total_income > 0:
                pie = pd.DataFrame({
                    'Type': ['Expenses', 'Remaining'],
                    'Value': [total_expenses, remaining]
                })
                fig, ax = plt.subplots()
                ax.pie(pie['Value'], labels=pie['Type'], autopct='%1.1f%%', startangle=90)
                ax.axis("equal")
                st.pyplot(fig)
            else:
                st.info("Add income to see chart.")
        else:
            st.warning("No data to display.")

    # Investment Suggestions
    elif section == "Investment Suggestions":
        st.title("📈 Age-based Investment Suggestions")
        st.markdown("""
        - **5–12 years**: Piggy Banks, Recurring Deposits (with parents)
        - **13–17 years**: Savings Account, Mutual Funds (with guardians), SIPs
        - **18–21 years**: Mutual Funds, Stock Market Basics, Digital Gold
        - **22–35 years**: Stocks, Crypto (carefully), NPS, PPF
        """)
        age_input = st.slider("Select Age for Suggestions", 5, 35, 18)
        if age_input <= 12:
            st.info("Recommended: Piggy Bank, Recurring Deposit")
        elif age_input <= 17:
            st.info("Recommended: Mutual Funds with guardian, SIPs, Savings Account")
        elif age_input <= 21:
            st.info("Recommended: Stock Basics, Digital Gold, SIPs")
        else:
            st.info("Recommended: Diversified Portfolio – Stocks, Mutual Funds, PPF, NPS")

    # Financial Education
    elif section == "Financial Education":
        st.title("📘 Financial Education Center")
        st.subheader("💹 What is a Mutual Fund?")
        st.markdown("""
        A **Mutual Fund** pools money from investors to invest in stocks, bonds, or other assets.
        - **Types**: Equity, Debt, Hybrid, Index, Liquid Funds
        """)

        st.subheader("📊 What is a Stock?")
        st.markdown("""
        A **Stock** represents a share in the ownership of a company.
        - **Types**: Common Stock, Preferred Stock, Growth Stock, Dividend Stock
        """)

        st.subheader("📈 What is Compounding?")
        st.markdown("""
        Compounding is the process where the value of an investment increases because the earnings also earn returns.
        """)

        st.subheader("🧠 What is Risk Appetite?")
        st.markdown("""
        Risk appetite is the amount of risk you're willing to take for potential returns.
        - **Low**: Prefer stable returns (FDs, Bonds)
        - **High**: Comfortable with volatility (Stocks, Crypto)
        """)
