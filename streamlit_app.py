import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime

st.set_page_config(page_title="Student Wealth & Investment Hub", layout="wide", page_icon="💰")

# ✅ Load Data Function - this handles file creation if not found
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("student_budget_data.csv", parse_dates=['Date'])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Date", "Income", "Expenses", "Category", "Amount", "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Assets", "Liabilities"])
        df.to_csv("student_budget_data.csv", index=False)
    return df

# ✅ Save Data Function
def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

# ✅ Load the CSV data
budget_data = load_data()

# Sidebar Navigation
st.sidebar.title("📚 Student Financial Toolkit")
section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Analysis", "Wealth Tracker", "Investment Suggestions", "Finance Education"])

# Sidebar Education Section
st.sidebar.markdown("""
---
### 📘 Finance Education
- **Types of Stocks**:
  - Blue-chip (stable)
  - Growth (high potential)
  - Dividend (income)
  - Penny stocks (high risk)

- **Types of Mutual Funds**:
  - Equity (high growth)
  - Debt (stable returns)
  - Hybrid (balanced)

- **Risk Levels**:
  - Low: PPF, FDs
  - Moderate: Index Funds, SIPs
  - High: Stocks, Crypto

- **Key Concepts**:
  - Net Worth = Assets - Liabilities
  - Diversification = Spreading risk
  - SIP = Systematic Investment Plan
""")

# Home Section
if section == "Home":
    st.title("🎓 Welcome to the Student Wealth & Investment Hub")
    st.markdown("""
    Track your **income**, monitor your **expenses**, set **savings goals**, and explore **investment opportunities** based on your age and risk appetite.

    #### Features:
    - Add income & expenses
    - View savings and category analysis
    - Net worth tracking
    - Personalized investment advice
    - Finance education sidebar
    """)

    st.subheader("📁 Current Budget Data")
    if not budget_data.empty:
        st.dataframe(budget_data)
    else:
        st.info("No data available. Please add entries.")

# Add Entry Section
elif section == "Add Entry":
    st.title("➕ Add Financial Entry")
    with st.form("entry_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=5, max_value=25)
        date = st.date_input("Date", value=datetime.today())
        income = st.number_input("Monthly Income ($)", min_value=0.0, format="%.2f")
        expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, format="%.2f")
        category = st.selectbox("Expense Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("Category Expense Amount ($)", min_value=0.0, format="%.2f")
        saving_goals = st.text_input("Saving Goals")
        risk_appetite = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"])
        investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"])
        assets = st.number_input("Total Assets ($)", min_value=0.0, format="%.2f")
        liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add Entry")

        if submit:
            new_row = pd.DataFrame([[name, date, income, expenses, category, amount, saving_goals, risk_appetite, investment_plan, age, assets, liabilities]],
                                   columns=["Name", "Date", "Income", "Expenses", "Category", "Amount", "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Assets", "Liabilities"])
            budget_data = pd.concat([budget_data, new_row], ignore_index=True)
            save_data(budget_data)
            st.success("✅ Entry added successfully!")

# Analysis Section
elif section == "Analysis":
    st.title("📊 Financial Overview")
    if not budget_data.empty:
        selected_name = st.selectbox("Select Student", budget_data['Name'].unique())
        student_data = budget_data[budget_data['Name'] == selected_name]

        total_income = student_data['Income'].sum()
        total_expenses = student_data['Expenses'].sum()
        total_savings = total_income - total_expenses

        st.metric("Total Income", f"${total_income:.2f}")
        st.metric("Total Expenses", f"${total_expenses:.2f}")
        st.metric("Estimated Savings", f"${total_savings:.2f}")

        category_summary = student_data.groupby("Category")["Amount"].sum()
        st.subheader("Spending by Category")
        st.bar_chart(category_summary)
    else:
        st.info("No data available.")

# Wealth Tracker Section
elif section == "Wealth Tracker":
    st.title("💼 Personal Wealth Overview")
    if not budget_data.empty:
        selected_name = st.selectbox("Select Student", budget_data['Name'].unique())
        student_data = budget_data[budget_data['Name'] == selected_name]

        assets = student_data['Assets'].sum()
        liabilities = student_data['Liabilities'].sum()
        net_worth = assets - liabilities

        st.metric("Total Assets", f"${assets:.2f}")
        st.metric("Total Liabilities", f"${liabilities:.2f}")
        st.metric("Net Worth", f"${net_worth:.2f}")

        st.subheader("Wealth Composition")
        pie = pd.DataFrame({
            'Type': ['Assets', 'Liabilities'],
            'Value': [assets, liabilities]
        })
        fig, ax = plt.subplots()
        ax.pie(pie['Value'], labels=pie['Type'], autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)
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

# Finance Education Section
elif section == "Finance Education":
    st.title("📘 Financial Literacy & Investment Knowledge")
    st.markdown("""
    #### 🧾 Understanding Stock Types:
    - **Blue-chip**: Reliable, established companies
    - **Growth Stocks**: Companies expected to grow faster
    - **Dividend Stocks**: Provide regular income
    - **Penny Stocks**: High risk, low price

    #### 📊 Types of Mutual Funds:
    - **Equity Funds**: Invest in stocks
    - **Debt Funds**: Invest in bonds or fixed-income instruments
    - **Hybrid Funds**: Mix of equity and debt

    #### ⚠️ Investment Risks:
    - Market Risk
    - Credit Risk
    - Liquidity Risk
    - Inflation Risk

    #### 📈 Popular Investment Tools:
    - SIPs (Systematic Investment Plans)
    - Index Funds
    - PPF (Public Provident Fund)
    - NPS (National Pension Scheme)

    #### 💡 Golden Rules:
    - Start early
    - Diversify your portfolio
    - Match investments to goals
    - Monitor and adjust regularly
    """)
