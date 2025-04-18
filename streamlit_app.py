import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta

# --- Must be the first Streamlit command ---
st.set_page_config(page_title="Student Budget & Investment Manager", layout="wide", page_icon="💸")

# --- Session State Initialization ---
if 'budget_data' not in st.session_state:
    st.session_state['budget_data'] = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}

# --- Sidebar ---
st.sidebar.title("📚 Student Financial Toolkit")
st.sidebar.markdown("---")
st.sidebar.header("📋 Navigation")
section = st.sidebar.radio("Choose a section", [
    "Home", "Add Expense", "Investments", "Nifty Tracker", "FAQ"])

st.sidebar.markdown("---")
st.sidebar.header("🧪 Sample Data")
if st.sidebar.checkbox("Load Dummy Data"):
    categories = ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"]
    today = datetime.today()
    dummy_entries = [
        [today - timedelta(days=random.randint(0, 30)),
         random.choice(categories),
         round(random.uniform(5.0, 100.0), 2)]
        for _ in range(30)
    ]
    dummy_df = pd.DataFrame(dummy_entries, columns=["Date", "Category", "Amount"])
    st.session_state['budget_data'] = pd.concat([st.session_state['budget_data'], dummy_df], ignore_index=True)
    st.sidebar.success("✅ Dummy data loaded!")

# --- Home Section ---
if section == "Home":
    st.title("🎓 Student Budget & Investment Manager")
    st.markdown("""
    Welcome to your personal finance tracker and investment planner!

    **Who Should Use This App?**
    - Students looking to control and monitor daily spending.
    - Individuals new to investing who want a simple simulator.
    - Anyone who wants to track Nifty 50 trends and manage finances.
    """)

    st.subheader("🔐 Enter Your Details")
    with st.form("user_info_form"):
        name = st.text_input("Name")
        budget = st.number_input("Monthly Budget ($)", min_value=0.0)
        submit_user = st.form_submit_button("Save")
        if submit_user:
            st.session_state['user_info'] = {"name": name, "budget": budget}
            st.success("Details saved!")

    if st.session_state['user_info']:
        st.markdown(f"### 👋 Hello, **{st.session_state['user_info']['name']}**!")
        st.markdown(f"💰 Monthly Budget: **${st.session_state['user_info']['budget']}**")

    if not st.session_state['budget_data'].empty:
        df = st.session_state['budget_data']
        df['Date'] = pd.to_datetime(df['Date'])
        grouped = df.groupby('Category')['Amount'].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📌 Spending by Category")
            fig1, ax1 = plt.subplots()
            ax1.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.subheader("📅 Daily Spending")
            daily_sum = df.groupby('Date')['Amount'].sum()
            fig2, ax2 = plt.subplots()
            ax2.plot(daily_sum.index, daily_sum.values, marker='o')
            ax2.set_title("Spending Over Time")
            ax2.set_ylabel("Amount ($)")
            st.pyplot(fig2)

        st.subheader("📊 Category Breakdown")
        st.bar_chart(grouped)
    else:
        st.info("No expenses yet. Go to 'Add Expense' to get started.")

# --- Add Expense Section ---
elif section == "Add Expense":
    st.title("➕ Add an Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add")
        if submit:
            new_data = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
            st.session_state['budget_data'] = pd.concat([st.session_state['budget_data'], new_data], ignore_index=True)
            st.success("✅ Expense added!")

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

# --- Nifty Tracker ---
elif section == "Nifty Tracker":
    st.title("📊 Nifty 50 Index Tracker")
    data = yf.download("^NSEI", period="1mo", interval="1d")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines+markers', name='Nifty 50'))
    fig.update_layout(title='Nifty 50 - Last 1 Month', xaxis_title='Date', yaxis_title='Index Value')
    st.plotly_chart(fig, use_container_width=True)

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
