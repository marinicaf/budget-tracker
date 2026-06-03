import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

def get_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open("budget-tracker-data").sheet1

def get_next_id(sheet):
    return len(sheet.get_all_values())

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def add_transaction(sheet, type, category, amount, description):
    next_id = get_next_id(sheet)
    time_added = get_timestamp()
    sheet.append_row([next_id, time_added, type, category, amount, description])

def load_transactions(sheet):
    data = sheet.get_all_values()
    headers = data[0]
    rows = data[1:]
    return headers, rows

sheet = get_sheet()
headers, rows = load_transactions(sheet)

# Sidebar
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Home", "Add Transaction", "View Transactions"])

# Load data
headers, rows = load_transactions(sheet)

if page == "Home":
    st.title("Budget Tracker")
    st.write("Welcome to your budget tracker!")

    # Summary
    st.subheader("Summary")

    type_idx = headers.index("type")
    amount_idx = headers.index("amount")

    total_income = sum(float(r[amount_idx]) for r in rows if r[type_idx] == "income")
    total_expense = sum(float(r[amount_idx]) for r in rows if r[type_idx] == "expense")
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"£{total_income:.2f}")
    col2.metric("Total Expense", f"£{total_expense:.2f}")
    col3.metric("Balance", f"£{balance:.2f}")

elif page == "Add Transaction":
    #Add transaction
    st.title("Add Transaction")

    type = st.selectbox("Type", ["income","expense"])
    category = st.text_input("Category (eg. food, salary, rent)")
    amount = st.number_input("Amount (£)", min_value = 0.01, step = 0.01)
    description = st.text_input("Description")

    if st.button("Add"):
        if category and description:
            add_transaction(sheet, type, category, amount, description)
            st.success(f"Added: {type} of £{amount:.2f} ({category}) - {description}")
        else:
            st.error("Please fill in category and description")

elif page == "View Transactions":
    #Transactions table
    st.subheader("All transactions")
    if rows:
        st.table([headers] + rows)
    else:
        st.info("No transactions yet")

