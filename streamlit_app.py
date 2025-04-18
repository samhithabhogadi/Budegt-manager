import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import datetime
import hashlib

st.set_page_config(page_title="Student Wealth & Investment Hub", layout="wide", page_icon="💰")

# ✅ Load Data Function
@st.cache_data
def load_data():
    expected_columns = ["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Expense Category"]
    try:
        df = pd.read_csv("student_budget_data.csv", parse_dates=['Date'])
        if not all(col in df.columns for col in expected_columns):
            raise ValueError("Missing columns")
    except (FileNotFoundError, ValueError):
        df = pd.DataFrame(columns=expected_columns)
        df.to_csv("student_budget_data.csv", index=False)
    return df

# ✅ Save Data Function
def save_data(df):
    df.to_csv("student_budget_data.csv", index=False)

# ✅ Hashing Function for Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ Load the CSV data
budget_data = load_data()

# Session setup
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.hashed_password = ""

# User login and registration
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
                new_user = pd.DataFrame([[username, hashed_password, None, 0.0, 0.0, "", "", "", None, ""]],
                                         columns=["Username", "Password", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Expense Category"])
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

    # Sidebar Navigation
    st.sidebar.title("📚 Student Financial Toolkit")
    section = st.sidebar.radio("Navigate to", ["Home", "Add Entry", "Analysis", "Wealth Tracker", "Investment Suggestions", "Financial Education"])

    # Home Section
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

    # Add Entry Section
    elif section == "Add Entry":
        st.title("➕ Add Financial Entry")
        with st.form("entry_form"):
            age = st.number_input("Age", min_value=5, max_value=25)
            date = st.date_input("Date", value=datetime.today())
            income = st.number_input("Monthly Income ($)", min_value=0.0, format="%.2f")
            expenses = st.number_input("Total Monthly Expenses ($)", min_value=0.0, format="%.2f")

            saving_goals = st.text_input("Saving Goals")
            risk_appetite = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"])
            investment_plan = st.selectbox("Preferred Investment Plan", ["None", "Piggy Bank", "Fixed Deposit", "Mutual Funds", "Stocks", "Crypto"])
            assets = st.number_input("Total Assets ($)", min_value=0.0, format="%.2f")
            liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, format="%.2f")
            submit = st.form_submit_button("Add Entry")

            if submit:
                new_row = pd.DataFrame([[username, date, income, expenses, saving_goals, risk_appetite, investment_plan, age, assets, liabilities]],
                                       columns=["Name", "Date", "Income", "Expenses", "Saving Goals", "Risk Appetite", "Investment Plan", "Age", "Assets", "Liabilities"])
                budget_data = pd.concat([budget_data, new_row], ignore_index=True)
                save_data(budget_data)
                st.success("✅ Entry added successfully!")

    # Analysis Section
    elif section == "Analysis":
        st.title("📊 Financial Overview")
        student_data = budget_data[budget_data['Name'] == username]
        if not student_data.empty:
            total_income = student_data['Income'].sum()
            total_expenses = student_data['Expenses'].sum()
            total_savings = total_income - total_expenses

            st.metric("Total Income", f"${total_income:.2f}")
            st.metric("Total Expenses", f"${total_expenses:.2f}")
            st.metric("Estimated Savings", f"${total_savings:.2f}")

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

            st.metric("Total Income", f"${total_income:.2f}")
            st.metric("Total Expenses", f"${total_expenses:.2f}")
            st.metric("Remaining Wealth", f"${remaining:.2f}")

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
        st.title("📈 Smart Investment Ideas for Your Age Group")
        age_input = st.slider("Select Your Age", 5, 35, 18)

        if age_input <= 12:
            st.info("👶 **5–12 years**\n- 🐖 Piggy Banks\n- 🏦 Recurring Deposits (with parents)\n✅ *Learn to save*")
        elif age_input <= 17:
            st.info("👦👧 **13–17 years**\n- 🏦 Savings Account\n- 📊 Mutual Funds (with guardians)\n- 🔄 SIPs\n✅ *Start small and steady*")
        elif age_input <= 21:
            st.info("🧑 **18–21 years**\n- 📈 Mutual Funds\n- 📚 Stock Market Basics\n- 💰 Digital Gold\n✅ *Build financial habits*")
        else:
            st.info("👨‍🎓 **22–35 years**\n- 📉 Stocks\n- 🪙 Crypto (risky)\n- 🛡️ NPS\n- 🌳 PPF\n✅ *Plan long-term & diversify*")

    # Financial Education
    elif section == "Financial Education":
        st.title("📚 Financial Education")
        st.markdown("""
        **What is a Mutual Fund?**
        - A professionally managed investment fund that pools money from many investors.

        **Types of Mutual Funds:**
        - Equity Funds, Debt Funds, Hybrid Funds, Index Funds

        **What are Stocks?**
        - Shares that represent ownership in a company.

        **Types of Stocks:**
        - **Blue Chip Stocks**: Large, reputable companies; low risk. Ideal for conservative investors.
        - **Growth Stocks**: Companies expected to grow rapidly; moderate to high risk. Best for long-term investors.
        - **Penny Stocks**: Very low-priced, speculative; high risk. Suitable only for aggressive investors.
        - **Dividend Stocks**: Pay regular income; moderate risk. Ideal for income-seeking investors.
        - **Cyclical Stocks**: Dependent on economic cycles; variable risk. Suitable for market-savvy investors.

        **Age-wise Stock Strategy:**
        - **18-21 years**: Focus on learning — invest in low-cost index funds or mutual funds. Understand basics before entering direct stocks.
        - **22-25 years**: Begin exploring stocks with a long-term growth horizon. Prefer blue-chip and growth stocks.
        - **26-30 years**: Diversify into mid-cap and sectoral stocks. Consider SIPs in equities and retirement-oriented funds.
        - **31-35 years**: Stabilize your portfolio. Increase allocation to dividend stocks and debt instruments. Focus on wealth preservation and tax-saving investments.

        **What is Risk Appetite?**
        - Your willingness to take investment risks for potential higher returns.

        **What is Compounding?**
        - Earning returns on your initial investment and the returns it generates over time.
        """)
