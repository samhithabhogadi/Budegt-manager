import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime
import hashlib

st.set_page_config(page_title="Student Wealth & Investment Hub", layout="wide", page_icon="💰")

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

def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

budget_data = load_data()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.hashed_password = ""

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

    st.sidebar.title("📚 Student Financial Toolkit")
    section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Wealth Tracker", "Investment Suggestions", "Financial Education"])

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

    elif section == "Wealth Tracker":
        st.title("📉 Expense vs Wealth Tracker")

        monthly_income_total = user_data["Monthly Income"].sum()
        total_expenses = user_data["Monthly Expenses"].sum() + user_data["Daily Expenses"].sum() + user_data["Amount (₹)"].sum()
        remaining_wealth = monthly_income_total - total_expenses

        st.metric("📈 Total Income", f"₹{monthly_income_total:,.2f}")
        st.metric("📉 Total Expenses", f"₹{total_expenses:,.2f}")
        st.metric("💰 Remaining Wealth", f"₹{remaining_wealth:,.2f}")

        pie_labels = ['Monthly Expenses', 'Daily Expenses', 'Other Expenses', 'Remaining']
        pie_values = [
            user_data["Monthly Expenses"].sum(),
            user_data["Daily Expenses"].sum(),
            user_data["Amount (₹)"].sum(),
            remaining_wealth if remaining_wealth > 0 else 0
        ]

        pie_chart = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values, hole=0.3)])
        st.plotly_chart(pie_chart, use_container_width=True)

        st.subheader("📊 Investment Strategy by Age & Risk")
        age = int(user_data["Age"].dropna().iloc[-1]) if not user_data["Age"].dropna().empty else 20
        risk = user_data["Risk Appetite"].dropna().iloc[-1] if not user_data["Risk Appetite"].dropna().empty else "Moderate"

        strategy = ""
        if age < 18:
            strategy = "Short-term: Piggy bank, Recurring Deposits.\n\nLong-term: Start saving discipline, learn about money."
        elif 18 <= age < 22:
            if risk == "Low":
                strategy = "Short-term: Fixed Deposits, Debt Funds.\n\nLong-term: Balanced Mutual Funds."
            elif risk == "Moderate":
                strategy = "Short-term: Debt Funds, Conservative Hybrid Funds.\n\nLong-term: Mutual Funds, Index Funds."
            else:
                strategy = "Short-term: Liquid ETFs, Digital Gold.\n\nLong-term: Stocks, Crypto (careful)."
        else:
            if risk == "Low":
                strategy = "Short-term: Debt Funds, Fixed Deposits.\n\nLong-term: PPF, Government Bonds."
            elif risk == "Moderate":
                strategy = "Short-term: Hybrid Funds.\n\nLong-term: Equity Mutual Funds, SIPs."
            else:
                strategy = "Short-term: Stocks, Thematic ETFs.\n\nLong-term: Equity, Real Estate Investment Trusts (REITs), Derivatives (if skilled)."

        st.markdown(f"""
        ### 🌎 Your Age: {age} | Risk Appetite: {risk}
        
        **Suggested Investment Strategy:**

        {strategy}
        """)
