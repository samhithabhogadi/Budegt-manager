import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import yfinance as yf

# ⚠️ Page config - keep this FIRST
st.set_page_config(page_title="Student Budget & Investment Manager", layout="wide", page_icon="💸")

# Load CSV
@st.cache_data
def load_data():
    return pd.read_csv("student_budget_data.csv", parse_dates=['Date'])

# Load and clean data
df = load_data()
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar Setup
with st.sidebar:
    st.title("📚 Financial Toolkit")
    st.markdown("Manage your **expenses & investments** all in one place.")
    selected_section = st.radio("Navigate to", ["Home", "Add Expense", "Investments", "Nifty Tracker", "FAQ"])
    selected_user = st.selectbox("Select Student", df['Name'].unique())
    st.markdown("---")
   

# Filter by user
user_data = df[df['Name'] == selected_user]

# Home Section
if selected_section == "Home":
    st.title(f"🎓 Welcome {selected_user}!")
    st.markdown("Here’s a snapshot of your budget and investment activities.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧾 Spending Breakdown by Category")
        category_spend = user_data.groupby("Category")['Amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_spend, labels=category_spend.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.subheader("📅 Spending Over Time")
        time_series = user_data.groupby('Date')['Amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.plot(time_series.index, time_series.values, marker='o')
        ax2.set_title("Daily Spending")
        ax2.set_ylabel("Amount ($)")
        st.pyplot(fig2)

    st.subheader("💼 Investment Plan Distribution")
    plan_count = user_data['Investment Plan'].value_counts()
    st.bar_chart(plan_count)

# Add Expense Section
elif selected_section == "Add Expense":
    st.title("➕ Add New Expense")
    with st.form("add_expense"):
        name = st.selectbox("Name", df['Name'].unique())
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("Amount", min_value=0.0, step=10.0)
        plan = st.selectbox("Investment Plan", ["Stocks", "Crypto", "Mutual Funds", "Fixed Deposit", "NPS"])
        submit = st.form_submit_button("Add")
        if submit:
            new_row = pd.DataFrame([[name, date, category, amount, plan]],
                                   columns=['Name', 'Date', 'Category', 'Amount', 'Investment Plan'])
            new_df = pd_
# --- Investment Planner ---
elif section == "Investments":
    st.title("📈 Investment Planner")
    st.markdown("Simulate future investment returns.")
    amount = st.number_input("Amount to invest ($)", min_value=100.0, step=50.0)
    years = st.slider("Investment Duration (Years)", 1, 10, 3)
    rate = st.slider("Expected Annual Return (%)", 5, 15, 8)

    if st.button("Calculate"):
        future_value = amount * ((1 + rate / 100) ** years)
        st.success(f"💹 In {years} years, your investment could grow to **${future_value:,.2f}**")

# --- FAQ ---
elif section == "FAQ":
    st.title("❓ Frequently Asked Questions")
    st.markdown("""
    **Q1: Who can use this app?**  
    A: Any student or beginner wanting to manage expenses and understand investments.

    **Q2: Is my data saved permanently?**  
    A: No, data is stored in memory per session. For permanent storage, use database integration.

    **Q3: How accurate is the investment planner?**  
    A: It uses compound interest calculations. It's for educational use only, not financial advice.

    **Q4: Can I track stocks other than Nifty 50?**  
    A: Not yet. But we plan to support custom tickers in the future.
    """)


