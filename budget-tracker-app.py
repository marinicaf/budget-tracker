import streamlit as st
import csv
import os
from datetime import datetime

FILENAME = "transactions.csv"

def setup_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME,"w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "time_added", "type", "category", "amount", "description"])

def get_next_id():
    with open(FILENAME, "r") as f:
        rows = list(csv.reader(f))
        return len(rows)

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def add_transaction(type, category, amount, description):
    next_id = get_next_id()
    time_added = get_timestamp()
    with open(FILENAME, "a", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow([next_id, time_added, type, category, amount, description])

def load_transactions():
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
        return headers, rows

def get_column_index(headers, name):
    return headers.index(name)

setup_file()

# Sidebar
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Home", "Add Transaction", "View Transactions"])

# Load data
headers, rows = load_transactions()

if page == "Home":
    st.title("Budget Tracker")
    st.write("Welcome to your budget tracker!")

    # Summary
    st.subheader("Summary")

    type_idx = get_column_index(headers, "type")
    amount_idx = get_column_index(headers, "amount")

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
            add_transaction(type, category, amount, description)
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

