import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Student Budget Manager", layout="wide", page_icon="💸")

# Sidebar Navigation
st.sidebar.title("📚 Student Budget Manager")
st.sidebar.markdown("---")
st.sidebar.subheader("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Budget", "Analytics"])

# Sidebar Details
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info("""
This app helps students manage their monthly expenses, track spending habits, and stay on budget.
Created using
""")

# Initialize session state
if 'budget_data' not in st.session_state:
    st.session_state['budget_data'] = pd.DataFrame(columns=['Date', 'Category', 'Amount'])

# Home Section
if section == "Home":
    st.title("🎓 Welcome to Your Student Budget Manager")
    st.markdown("""
    Stay on top of your finances! Use this app to:
    - Track daily expenses
    - Visualize spending patterns
    - Plan your monthly budget
    """)
    st.image("https://cdn.pixabay.com/photo/2017/09/04/18/40/money-2712935_960_720.jpg", use_column_width=True)

# Add Expense Section
elif section == "Add Expense":
    st.title("➕ Add a New Expense")
    with st.form(key='expense_form'):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("Amount (in $)", min_value=0.0, format="%.2f")
        submit = st.form_submit_button(label='Add Expense')

        if submit:
            new_data = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
            st.session_state['budget_data'] = pd.concat([st.session_state['budget_data'], new_data], ignore_index=True)
            st.success("Expense added successfully!")

# View Budget Section
elif section == "View Budget":
    st.title("📋 Your Budget Records")
    if st.session_state['budget_data'].empty:
        st.warning("No expenses recorded yet.")
    else:
        st.dataframe(st.session_state['budget_data'].sort_values(by='Date', ascending=False), use_container_width=True)

# Analytics Section
elif section == "Analytics":
    st.title("📊 Budget Analytics")
    if st.session_state['budget_data'].empty:
        st.warning("No data to visualize yet.")
    else:
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

        st.markdown("---")
        st.subheader("Category Breakdown")
        st.bar_chart(grouped)


