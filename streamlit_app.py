import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import yfinance as yf
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
        df = pd.DataFrame(columns=["Name", "Date","income", "Expenses","Category", "Amount", "Saving Goals","Risk Appetite", "Investment Plan", "Age"])
        df.to_csv("student_budget_data.csv", index=False)
    return df

# wm 
net_worth = total_assets - total_liabilities
st.metric("📈 Net Worth", f"${net_worth:.2f}")

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
# risk app 
risk = st.selectbox("What's your risk appetite?", ["Low", "Moderate", "High"])
if risk == "Low":
    st.info("Recommended: Fixed Deposits, PPF, Bonds")
elif risk == "Moderate":
    st.info("Recommended: Mutual Funds, Index Funds")
else:
    st.info("Recommended: Stocks, Crypto, Real Estate")

# ✅ Save Data Function
def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

# ✅ Load the CSV data after defining the functions above
budget_data = load_data()

# Sidebar Navigation
st.sidebar.title("📚 Student Financial Toolkit")
section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Analysis", "Investment Suggestions"])

# Home Section
if section == "Home":
    st.title("🎓 Welcome to the Student Budget & Investment Manager")
    st.markdown("""
    Track your **pocket money**, monitor your **expenses**, and explore **investment options** suitable for your age!

    #### Features:
    - Add pocket money & expenses
    - View expense distribution
    - Get age-based investment advice
    """)

    st.subheader("📁 Current Budget Data")
    if not budget_data.empty:
        st.dataframe(budget_data)
    else:
        st.info("No data available. Please add entries.")

# Add Entry Section
elif section == "Add Entry":
    st.title("➕ Add Pocket Money & Expense")
    with st.form("entry_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=5, max_value=25)
        date = st.date_input("Date", value=datetime.today())
        pocket_money = st.number_input("Pocket Money Received ($)", min_value=0.0, format="%.2f")
        category = st.selectbox("Expense Category", ["Food", "Transport", "Rent", "Entertainment", "Utilities", "Others"])
        amount = st.number_input("Expense Amount ($)", min_value=0.0, format="%.2f")
        investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"])
        submit = st.form_submit_button("Add Entry")

        if submit:
            new_row = pd.DataFrame([[name, date, category, amount, pocket_money, investment_plan, age]],
                                   columns=["Name", "Date", "Category", "Amount", "Pocket Money", "Investment Plan", "Age"])
            budget_data = pd.concat([budget_data, new_row], ignore_index=True)
            save_data(budget_data)
            st.success("✅ Entry added successfully!")

# Analysis Section
elif section == "Analysis":
    st.title("📊 Pocket Money vs Expenses Analysis")
    if not budget_data.empty:
        selected_name = st.selectbox("Select Student", budget_data['Name'].unique())
        student_data = budget_data[budget_data['Name'] == selected_name]

        total_pocket = student_data['Pocket Money'].sum()
        total_spent = student_data['Amount'].sum()
        saved_money = total_pocket - total_spent

        st.metric("Total Pocket Money", f"${total_pocket:.2f}")
        st.metric("Total Spent", f"${total_spent:.2f}")
        st.metric("Saved Money", f"${saved_money:.2f}")

        category_summary = student_data.groupby("Category")["Amount"].sum()
        st.subheader("Spending by Category")
        st.bar_chart(category_summary)
    else:
        st.info("No data available.")

# Investment Suggestions
elif section == "Investment Suggestions":
    st.title("💼 Age-based Investment Suggestions")
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
