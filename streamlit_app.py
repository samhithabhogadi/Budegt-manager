import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta

# Dummy Data Setup
if st.sidebar.checkbox("🧪 Load Sample Data"):
    categories = ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"]
    today = datetime.today()

    dummy_entries = []
    for _ in range(30):
        date = today - timedelta(days=random.randint(0, 30))
        category = random.choice(categories)
        amount = round(random.uniform(5.0, 100.0), 2)
        dummy_entries.append([date, category, amount])

    dummy_df = pd.DataFrame(dummy_entries, columns=["Date", "Category", "Amount"])
    st.session_state['budget_data'] = pd.concat([st.session_state['budget_data'], dummy_df], ignore_index=True)
    st.success("✅ Dummy data loaded successfully!")


st.set_page_config(page_title="Student Budget & Investment Manager", layout="wide", page_icon="💸")

# Sidebar Navigation
st.sidebar.title("📚 Student Financial Toolkit")
section = st.sidebar.radio("Navigate to", ["Home", "Add Expense", "Investments", "Nifty Tracker"])

# Session State Initialization
if 'budget_data' not in st.session_state:
    st.session_state['budget_data'] = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}

# Home Section
if section == "Home":
    st.title("🎓 Welcome to Student Budget & Investment Manager")

    with st.form("user_info_form"):
        st.subheader("🔐 Enter Your Details")
        name = st.text_input("Name")
        budget = st.number_input("Monthly Budget ($)", min_value=0.0)
        submit_user = st.form_submit_button("Save Details")
        if submit_user:
            st.session_state['user_info'] = {"name": name, "budget": budget}
            st.success("Details saved!")

    if st.session_state['user_info']:
        st.markdown(f"### Hello, **{st.session_state['user_info']['name']}**!")
        st.markdown(f"💰 Your Monthly Budget: **${st.session_state['user_info']['budget']}**")

        if not st.session_state['budget_data'].empty:
            df = st.session_state['budget_data']
            df['Date'] = pd.to_datetime(df['Date'])
            grouped = df.groupby('Category')['Amount'].sum()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Total Spending by Category")
                fig1, ax1 = plt.subplots()
                ax1.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=90)
                ax1.axis('equal')
                st.pyplot(fig1)

            with col2:
                st.subheader("Spending Over Time")
                daily_sum = df.groupby('Date')['Amount'].sum()
                fig2, ax2 = plt.subplots()
                ax2.plot(daily_sum.index, daily_sum.values, marker='o')
                ax2.set_title("Daily Spending")
                ax2.set_ylabel("Amount ($)")
                st.pyplot(fig2)

            st.subheader("📊 Category Breakdown")
            st.bar_chart(grouped)
        else:
            st.info("No expenses added yet. Head to 'Add Expense' to begin tracking.")

# Add Expense Section
elif section == "Add Expense":
    st.title("➕ Add an Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add Expense")
        if submit:
            new_data = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
            st.session_state['budget_data'] = pd.concat([st.session_state['budget_data'], new_data], ignore_index=True)
            st.success("Expense added successfully!")

# Investment Section
elif section == "Investments":
    st.title("📈 Investment Planner")
    st.markdown("Use this section to simulate simple investments.")

    amount_to_invest = st.number_input("Enter amount to invest ($)", min_value=100.0, step=50.0)
    years = st.slider("Investment Duration (Years)", 1, 10, 3)
    expected_rate = st.slider("Expected Annual Return (%)", 5, 15, 8)

    if st.button("Calculate Future Value"):
        future_value = amount_to_invest * ((1 + (expected_rate / 100)) ** years)
        st.success(f"💹 In {years} years, your investment could grow to: ${future_value:,.2f}")

# Nifty 50 Tracker Section
elif section == "Nifty Tracker":
    st.title("📊 Nifty 50 Index Tracker")
    ticker = "^NSEI"
    data = yf.download(ticker, period="1mo", interval="1d")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines+markers', name='Nifty 50'))
    fig.update_layout(title='Nifty 50 - Last 1 Month', xaxis_title='Date', yaxis_title='Index Value')
    st.plotly_chart(fig, use_container_width=True)
