import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime

st.set_page_config(page_title="Student Wealth & Investment Hub", layout="wide", page_icon="💰")

# ✅ Load Data Function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("student_budget_data.csv", parse_dates=['Date'])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
        df.to_csv("student_budget_data.csv", index=False)
    return df

# ✅ Save Data Function
def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

# ✅ Load the CSV data
budget_data = load_data()

# Username input on main screen
st.header("👤 User Login")
username = st.text_input("Enter your name", key="username")

if not username:
    st.warning("Please enter your name to continue.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("📚 Student Financial Toolkit")
section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Analysis", "Wealth Tracker", "Investment Suggestions", "Financial Education"])

# Home Section
if section == "Home":
    st.title("🎓 Welcome to the Student Wealth & Investment Hub")
    st.markdown("""
    Track your **income**, monitor your **expenses**, set **savings goals**, and explore **investment opportunities** based on your age and risk appetite.

    #### Features:
    - Add income & multiple expenses
    - View savings and financial analysis
    - Net worth tracking
    - Personalized investment advice
    """)

    st.subheader("📁 Your Budget Data")
    user_data = budget_data[budget_data['Name'] == username]
    if not user_data.empty:
        latest_entry = user_data.sort_values("Date", ascending=False)
        st.dataframe(latest_entry)
    else:
        st.info("No data available. Please add entries.")

# Add Entry Section
elif section == "Add Entry":
    st.title("➕ Add Financial Entry")
    num_entries = st.number_input("How many entries do you want to add?", min_value=1, max_value=10, step=1)

    for i in range(int(num_entries)):
        st.markdown(f"### Entry {i+1}")
        with st.form(f"entry_form_{i}", clear_on_submit=True):
            age = st.number_input("Age", min_value=5, max_value=25, key=f"age_{i}")
            date = st.date_input("Date", value=datetime.today(), key=f"date_{i}")
            income = st.number_input("Monthly Income (₹)", min_value=0.0, format="%.2f", key=f"income_{i}")
            expenses = st.number_input("Total Monthly Expenses (₹)", min_value=0.0, format="%.2f", key=f"expenses_{i}")
            saving_goals = st.text_input("Saving Goals", key=f"savings_{i}")
            risk_appetite = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"], key=f"risk_{i}")
            investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"], key=f"plan_{i}")
            submit = st.form_submit_button("Add Entry")

            if submit:
                new_row = pd.DataFrame([[username, date, income, expenses, saving_goals, risk_appetite, investment_plan, age]],
                                       columns=["Name", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age"])
                budget_data = pd.concat([budget_data, new_row], ignore_index=True)
                save_data(budget_data)
                st.success(f"✅ Entry {i+1} added successfully!")

# Analysis Section
elif section == "Analysis":
    st.title("📊 Financial Overview")
    student_data = budget_data[budget_data['Name'] == username]
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

    else:
        st.info("No data available.")

# Wealth Tracker Section
elif section == "Wealth Tracker":
    st.title("💼 Expense vs Remaining Wealth")
    student_data = budget_data[budget_data['Name'] == username]
    if not student_data.empty:
        total_income = student_data['Income'].sum()
        total_expenses = student_data['Expenses'].sum()
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
    - **22-25 years**: Full-fledged Stocks, Crypto (carefully), NPS, PPF
    """)

    age_input = st.slider("Select Age for Suggestions", 5, 25, 18)
    if age_input <= 12:
        st.info("Recommended: Piggy Bank, Recurring Deposit")
    elif age_input <= 17:
        st.info("Recommended: Savings Account, Mutual Funds, SIP")
    elif age_input <= 21:
        st.info("Recommended: Mutual Funds, Stock Market Basics, Digital Gold")
    else:
        st.info("Recommended: Stocks, Crypto (cautiously), NPS, PPF")

    st.subheader("📌 Risk Appetite Based Suggestions")
    risk = st.selectbox("What's your risk appetite?", ["Low", "Moderate", "High"])
    if risk == "Low":
        st.info("Recommended: Fixed Deposits, PPF, Bonds")
    elif risk == "Moderate":
        st.info("Recommended: Mutual Funds, Index Funds")
    else:
        st.info("Recommended: Stocks, Crypto, Real Estate")

# Financial Education Section
elif section == "Financial Education":
    st.title("📖 Financial Education")

    st.subheader("📌 What is a Mutual Fund?")
    st.markdown("""
    A **mutual fund** is like a money pool where many people put in their money. This money is then managed by experts who use it to buy **stocks**, **bonds**, and other investments. 

    Everyone who puts money into the fund owns a small part of it. If the investments do well, everyone earns money. If they don’t do well, everyone shares the loss too. 

    It's a simple way for beginners to invest, because professionals make the big decisions for you.
    """)

    st.subheader("📌 Types of Mutual Funds")
    st.markdown("""
    - **Equity Funds**: Invest in stocks
    - **Debt Funds**: Invest in fixed income instruments
    - **Hybrid Funds**: Combine equity and debt
    - **Index Funds**: Track a stock market index
    """)

    st.subheader("📌 What is a Stock?")
    st.markdown("""
    A stock represents ownership in a company. When you own a stock, you're a shareholder of that company.
    """)

    st.subheader("📌 Types of Stocks")
    st.markdown("""
    - **Common Stocks**: Voting rights and dividends
    - **Preferred Stocks**: Priority in dividends, no voting rights
    - **Growth Stocks**: Companies expected to grow fast
    - **Dividend Stocks**: Provide regular income via dividends
    """)

    st.subheader("📌 What is Risk Appetite?")
    st.markdown("""
    Risk appetite is the level of risk you’re willing to take with your investments. It depends on your age, goals, and personality.
    """)

    st.subheader("📌 What is Compounding?")
    st.markdown("""
    Compounding means earning interest on both your original money and the interest that money earns. Over time, this has a snowball effect.
    """)

    st.subheader("📌 Budgeting Plan for Students")
    st.markdown("""
    - Allocate income using the 50/30/20 rule:
        - 50% Needs (Food, Travel)
        - 30% Wants (Entertainment)
        - 20% Savings/Investments
    - Track monthly expenses
    - Set realistic savings goals
    - Avoid debt accumulation
    - Start investing early in safe instruments
    """)
