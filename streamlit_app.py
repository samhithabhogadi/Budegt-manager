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

# Username and password input on main screen
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.hashed_password = ""

if not st.session_state.authenticated:
    st.header("👤 User Login")
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
        elif st.button("Register New User"):
            new_user = pd.DataFrame([[username, hashed_password, None, 0.0, 0.0, "", "", "", None]],
                                     columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
            budget_data = pd.concat([budget_data, new_user], ignore_index=True)
            save_data(budget_data)
            st.success("✅ New user registered. You can now start adding your data.")
else:
    username = st.session_state.username
    hashed_password = st.session_state.hashed_password
    user_data = budget_data[(budget_data['Username'] == username) & (budget_data['Password'] == hashed_password)]

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

    # Analysis Section
    elif section == "Analysis":
        st.title("📊 Financial Overview")
        if not user_data.empty:
            total_income = user_data['Income'].sum()
            total_expenses = user_data['Expenses'].sum()
            total_savings = total_income - total_expenses

            st.metric("Total Income", f"₹{total_income:.2f}")
            st.metric("Total Expenses", f"₹{total_expenses:.2f}")
            st.metric("Estimated Savings", f"₹{total_savings:.2f}")

            st.subheader("📈 Income vs Expenses Over Time")
            line_data = user_data.sort_values("Date")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=line_data['Date'], y=line_data['Income'], mode='lines+markers', name='Income'))
            fig.add_trace(go.Scatter(x=line_data['Date'], y=line_data['Expenses'], mode='lines+markers', name='Expenses'))
            st.plotly_chart(fig)
        else:
            st.info("No data available.")

    # Wealth Tracker Section
    elif section == "Wealth Tracker":
        st.title("💼 Expense vs Remaining Wealth")
        if not user_data.empty:
            total_income = user_data['Income'].sum()
            total_expenses = user_data['Expenses'].sum()
            remaining = total_income - total_expenses

            st.metric("Total Income", f"₹{total_income:.2f}")
            st.metric("Total Expenses", f"₹{total_expenses:.2f}")
            st.metric("Remaining Wealth", f"₹{remaining:.2f}")

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
                st.info("Insufficient income data to display chart.")
        else:
            st.warning("No data to display.")

    # Investment Suggestions
    elif section == "Investment Suggestions":
        st.title("📈 Age-based Investment Suggestions")
        st.markdown("""
        - **5-12 years**: Piggy Banks, Recurring Deposits (with parents)
        - **13-17 years**: Savings Account, Mutual Funds (with guardians), SIPs
        - **18-21 years**: Mutual Funds, Stock Market Basics, Digital Gold
        - **22-35 years**: Full-fledged Stocks, Crypto (carefully), NPS, PPF
        """)

        age_input = st.slider("Select Age for Suggestions", 5, 35, 18)
        if age_input <= 12:
            st.info("Recommended: Piggy Bank, Recurring Deposit")
        elif age_input <= 17:
            st.info("Recommended: Savings Account, Mutual Funds (with guardians), SIPs")
        elif age_input <= 21:
            st.info("Recommended: Mutual Funds, Stock Market Basics, Digital Gold")
        else:
            st.info("Recommended: Stocks, Crypto (carefully), NPS, PPF")

    # Financial Education Section
    elif section == "Financial Education":
        st.title("📖 Financial Education")
        st.markdown("""
        ### 💡 What is a Mutual Fund?
        A mutual fund pools money from many investors to invest in stocks, bonds, or other assets.

        **Types of Mutual Funds:**
        - Equity Funds
        - Debt Funds
        - Hybrid Funds
        - Index Funds

        ### 📈 What are Stocks?
        Stocks represent ownership in a company.

        **Types of Stocks:**
        - Common Stock
        - Preferred Stock
        - Large-cap, Mid-cap, Small-cap

        ### 🔍 What is Risk Appetite?
        Your risk appetite is the level of risk you're willing to take with your investments. It influences the types of investments suitable for you.

        ### 📊 What is Compounding?
        Compounding is when your investment earns returns, and those returns also earn returns over time. The earlier you start investing, the more you benefit!
        """)
