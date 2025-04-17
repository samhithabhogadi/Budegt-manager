import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Student Budget Manager", layout="wide", page_icon="💸")
if section == "🏠 Home":
    st.title("🎓 Welcome to Your Student Budget Dashboard")

    st.subheader("🧑 Personal Setup")
    user_name = st.text_input("Enter your name")
    monthly_budget = st.slider("Set your Monthly Budget ($)", min_value=100, max_value=5000, step=50, value=1000)

    if user_name:
        st.success(f"Hello {user_name}! 👋 Here’s how you’re doing with your budget of ${monthly_budget:.2f} this month.")
    else:
        st.info("Please enter your name above to personalize your dashboard.")

    st.markdown("___")

    if not st.session_state['budget_data'].empty:
        df = st.session_state['budget_data']
        df['Date'] = pd.to_datetime(df['Date'])
        grouped = df.groupby('Category')['Amount'].sum()
        daily_sum = df.groupby('Date')['Amount'].sum()
        total_spent = df['Amount'].sum()

        # Budget status message
        if user_name:
            if total_spent > monthly_budget:
                st.error(f"⚠️ {user_name}, you've exceeded your monthly budget by ${total_spent - monthly_budget:.2f}!")
            else:
                st.success(f"✅ {user_name}, you're within your budget. You have ${monthly_budget - total_spent:.2f} left.")

        # Metrics
        highest_category = grouped.idxmax()
        highest_amount = grouped.max()
        st.metric("💵 Total Spent", f"${total_spent:.2f}")
        st.metric("📌 Top Spending Category", f"{highest_category} (${highest_amount:.2f})")

        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🧁 Spending by Category")
            fig1, ax1 = plt.subplots()
            ax1.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.subheader("📅 Daily Spending Trend")
            fig2, ax2 = plt.subplots()
            ax2.plot(daily_sum.index, daily_sum.values, marker='o', color='green')
            ax2.set_title("Daily Spending Over Time")
            ax2.set_ylabel("Amount ($)")
            st.pyplot(fig2)

        st.markdown("---")
        st.subheader("📊 Interactive Category Breakdown")
        fig_bar = px.bar(
            grouped.reset_index(),
            x='Category',
            y='Amount',
            color='Amount',
            color_continuous_scale='Blues',
            labels={'Amount': 'Total Spent ($)', 'Category': 'Expense Category'},
            title="Expense Breakdown by Category"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info("No expenses yet. Add some in the ➕ Add Expense section to see insights!")
# Sidebar Navigation
st.sidebar.title("📚 Student Budget Manager")
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Navigation")
section = st.sidebar.radio("Go to", ["🏠 Home", "➕ Add Expense"])

# Sidebar Details
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About")
st.sidebar.info("""
This app helps students manage their monthly expenses, track spending habits, and stay on budget.

🔧 Built with:
- Python 🐍
- Streamlit 🌐
- Pandas 📊
- Matplotlib 📈
- Plotly 🔥
""")

# Initialize session state
if 'budget_data' not in st.session_state:
    st.session_state['budget_data'] = pd.DataFrame(columns=['Date', 'Category', 'Amount'])

# Home Section
if section == "🏠 Home":
    st.title("🎓 Welcome to Your Student Budget Dashboard")
    st.markdown("Gain insights into your spending patterns and make smarter financial decisions 💡")

    if not st.session_state['budget_data'].empty:
        df = st.session_state['budget_data']
        df['Date'] = pd.to_datetime(df['Date'])
        grouped = df.groupby('Category')['Amount'].sum()
        daily_sum = df.groupby('Date')['Amount'].sum()

        # Summary Stats
        total_spent = df['Amount'].sum()
        highest_category = grouped.idxmax()
        highest_amount = grouped.max()

        st.metric("💵 Total Spent", f"${total_spent:.2f}")
        st.metric("📌 Top Spending Category", f"{highest_category} (${highest_amount:.2f})")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🧁 Spending by Category")
            fig1, ax1 = plt.subplots()
            ax1.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.subheader("📅 Daily Spending Trend")
            fig2, ax2 = plt.subplots()
            ax2.plot(daily_sum.index, daily_sum.values, marker='o', color='green')
            ax2.set_title("Daily Spending Over Time")
            ax2.set_ylabel("Amount ($)")
            st.pyplot(fig2)

        st.markdown("---")
        st.subheader("📊 Interactive Category Breakdown")
        fig_bar = px.bar(
            grouped.reset_index(),
            x='Category',
            y='Amount',
            color='Amount',
            color_continuous_scale='Blues',
            labels={'Amount': 'Total Spent ($)', 'Category': 'Expense Category'},
            title="Expense Breakdown by Category"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.success("Tip: Consider reducing your expenses in the highest category!")

    else:
        st.info("No expenses yet. Add some in the ➕ Add Expense section to see insights!")

# Add Expense Section
elif section == "➕ Add Expense":
    st.title("📝 Log a New Expense")
    with st.form(key='expense_form'):
        date = st.date_input("📅 Date")
        category = st.selectbox("📂 Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("💰 Amount (in $)", min_value=0.0, format="%.2f")
        submit = st.form_submit_button(label='➕ Add Expense')

        if submit:
            new_data = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
            st.session_state['budget_data'] = pd.concat([st.session_state['budget_data'], new_data], ignore_index=True)
            st.success("✅ Expense added successfully!")
