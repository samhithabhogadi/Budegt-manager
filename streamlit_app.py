import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from streamlit_animate import st_animate

# Set the page config
st.set_page_config(page_title="Finora", layout="wide", page_icon="💼")

# Apply custom theme using markdown (Streamlit's native support is limited)
st.markdown(
    """
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6f9;
            color: #1f2937;
        }
        .stApp {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .block-container {
            padding: 1rem 2rem;
        }
        .css-1d391kg {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: white;
        }
        .css-1d391kg a {
            color: #d1d5db;
        }
        .css-1d391kg a:hover {
            color: white;
        }
        .scrollbox {
            overflow-x: auto;
            white-space: nowrap;
            padding: 10px;
            background: #f1f5f9;
            border: 1px dashed #cbd5e1;
            border-radius: 10px;
        }
        .section {
            border-left: 4px groove #4ade80;
            padding-left: 1rem;
            margin-bottom: 1.5rem;
            background: #f0fdf4;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Show opening welcome screen only once
if 'welcome_done' not in st.session_state:
    st.session_state['welcome_done'] = False

if not st.session_state['welcome_done']:
    st_animate("fadeIn", duration=500)
    st.title("💼 Welcome to Finora")
    st.subheader("Your smart companion for budgeting and wealth management ✨")
    st.markdown("Designed for students and young earners to build habits for a wealthy future.")
    if st.button("Enter App ➡️"):
        st_animate("bounceIn", duration=700)
        st.session_state['welcome_done'] = True
    st.stop()

# Initialize session state for app data
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount', 'Notes'])

if 'goals' not in st.session_state:
    st.session_state['goals'] = pd.DataFrame(columns=['Goal', 'Target Amount', 'Saved Amount', 'Deadline'])

if 'achievements' not in st.session_state:
    st.session_state['achievements'] = []

# Sidebar navigation
st.sidebar.title("📊 Finora")
st.sidebar.markdown("### Finance simplified ✨")
page = st.sidebar.radio("Navigate to", ["Dashboard", "Add Transaction", "Set Goals", "Reports", "Investment Suggestions"])

# Financial Education
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Financial Education")
st.sidebar.markdown("""
**Equity Investments**:
- Ownership in a company (stocks)
- Types: Large-cap, Mid-cap, Small-cap
- Suitable for long-term and higher risk takers

**Debt Investments**:
- Lending to institutions (bonds, FDs)
- Types: Government, Corporate, Bank FDs
- Best for risk-averse, fixed-income seekers
""")

# Add Transaction Page
if page == "Add Transaction":
    st.title("💸 Add Income or Expense")
    with st.form("transaction_form"):
        date = st.date_input("Date", datetime.today())
        t_type = st.selectbox("Type", ["Income", "Expense"])
        category = st.selectbox("Category", ["Salary", "Food", "Transport", "Rent", "Miscellaneous", "Investment"])
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%0.2f")
        notes = st.text_input("Notes")
        submitted = st.form_submit_button("Add Transaction")

        if submitted:
            new_row = pd.DataFrame([[date, t_type, category, amount, notes]],
                                   columns=['Date', 'Type', 'Category', 'Amount', 'Notes'])
            st.session_state['transactions'] = pd.concat([st.session_state['transactions'], new_row], ignore_index=True)
            st.success("Transaction added successfully!")

# Set Goals Page
elif page == "Set Goals":
    st.title("🎯 Set Savings Goals")
    with st.form("goal_form"):
        goal_name = st.text_input("Goal Name")
        target = st.number_input("Target Amount (₹)", min_value=100.0)
        saved = st.number_input("Current Saved Amount (₹)", min_value=0.0)
        deadline = st.date_input("Deadline")
        submitted = st.form_submit_button("Add Goal")

        if submitted:
            new_goal = pd.DataFrame([[goal_name, target, saved, deadline]],
                                    columns=['Goal', 'Target Amount', 'Saved Amount', 'Deadline'])
            st.session_state['goals'] = pd.concat([st.session_state['goals'], new_goal], ignore_index=True)
            st.success("Goal added!")

    st.subheader("Your Goals")
    st.dataframe(st.session_state['goals'])

# Dashboard Page
elif page == "Dashboard":
    st.title("📈 Dashboard")
    df = st.session_state['transactions']
    income = df[df['Type'] == 'Income']['Amount'].sum()
    expense = df[df['Type'] == 'Expense']['Amount'].sum()
    savings = income - expense

    st.markdown("### 💼 Summary", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{income:,.2f}")
    col2.metric("Total Expenses", f"₹{expense:,.2f}")
    col3.metric("Net Savings", f"₹{savings:,.2f}")

    if not df.empty:
        st.markdown("### 🧾 Recent Transactions")
        st.markdown('<div class="scrollbox">' + df.sort_values(by='Date', ascending=False).head(10).to_html(index=False) + '</div>', unsafe_allow_html=True)

# Reports Page
elif page == "Reports":
    st.title("📊 Expense Reports")
    df = st.session_state['transactions']
    if df.empty:
        st.warning("No transactions yet.")
    else:
        exp_df = df[df['Type'] == 'Expense']
        category_summary = exp_df.groupby('Category')['Amount'].sum().reset_index()

        st.subheader("Expenses by Category")
        st.bar_chart(category_summary.set_index('Category'))

        st.subheader("Monthly Trends")
        df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
        monthly = df.groupby(['Month', 'Type'])['Amount'].sum().unstack().fillna(0)
        st.pie_chart(monthly)

# Investment Suggestions Page
elif page == "Investment Suggestions":
    st.title("💡 Investment Suggestions")
    st.markdown("""
    Based on your savings and goals, consider these:
    - **SIPs in Mutual Funds** for long-term wealth.
    - **RDs or FDs** for short-term secure saving.
    - **Digital Gold** for goal-linked savings.
    - **PPF** if you’re risk-averse and want tax benefits.
    
    ✅ You can also link your goals to specific investments!
    """)

    # Investment Portfolio Integration (using Yahoo Finance)
    st.subheader("Track Your Investments")
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, etc.)", "AAPL")
    if stock_symbol:
        stock = yf.Ticker(stock_symbol)
        stock_data = stock.history(period="1d")
        st.write(f"**{stock_symbol} Stock Data**")
        st.dataframe(stock_data)

        closing_price = stock_data['Close'].iloc[-1]
        st.info(f"Last Closing Price of {stock_symbol}: ₹{closing_price:,.2f}")
        st.line_chart(stock_data['Close'])

    st.subheader("Your Financial Goals")
    st.dataframe(st.session_state['goals'])

    st.subheader("Savings Overview")
    income = st.session_state['transactions'][st.session_state['transactions']['Type'] == 'Income']['Amount'].sum()
    expense = st.session_state['transactions'][st.session_state['transactions']['Type'] == 'Expense']['Amount'].sum()
    savings = income - expense
    st.info(f"Estimated Available Savings: ₹{savings:,.2f}")

    if savings < 0:
        st.warning("You're spending more than you earn! Consider reviewing your expenses.")
