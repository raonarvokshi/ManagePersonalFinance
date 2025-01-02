import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


def add_expense():
    st.subheader("Add Expense")

    title = st.text_input("Title")
    amount = st.number_input("Expense Amount", min_value=0.0, step=0.01)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Add Expense"):

        if not title or not amount and not category and not description:
            st.error("Please fill out all the required fields!")

        elif title and category and description and amount == 0.0:
            st.error("Amount can not be 0")

        elif title and amount and category and description:
            json = {"user_id": st.session_state.user_id, "title": title, "amount": amount,
                    "category": category, "description": description}

            response = requests.post(
                f"{BASE_URL}/expenses/",
                json=json
            )

            if response.status_code == 200:
                st.success("Expense added successfully!")

            else:
                st.error(f"Failed to add expense. {response.text}")


def update_expense():
    st.subheader("Update Expense")

    response = requests.get(f"{BASE_URL}/expenses/",
                            params={"user_id": st.session_state.user_id})

    if response.status_code == 200:
        expenses = response.json()

        if expenses:
            expense_title = st.selectbox("Select Expense to Update", [
                expense["title"] for expense in expenses])

            selected_expense = next(
                (expense for expense in expenses if expense["title"] == expense_title))

            if selected_expense:
                new_title = st.text_input(
                    "New Title", value=selected_expense["title"])
                new_amount = st.number_input(
                    "New Amount", value=selected_expense["amount"])
                new_category = st.text_input(
                    "New Category", value=selected_expense["category"])
                new_description = st.text_area(
                    "New Description", value=selected_expense["description"])
                new_date = st.date_input("New Date", value=pd.to_datetime(
                    selected_expense["date"]).date())

                if st.button("Update Expense"):
                    json = {
                        "title": new_title,
                        "amount": new_amount,
                        "category": new_category,
                        "description": new_description,
                        "date": new_date.isoformat(),
                    }

                    update_response = requests.put(
                        f"{BASE_URL}/expenses/{selected_expense["id"]}", json=json)

                    if update_response.status_code == 200:
                        st.success("Expense Updated Successfully!")
                    else:
                        st.error(
                            f"Failed to update expense! Error: {update_response.text}")
        else:
            st.info("No Expenses To Update!")


def delete_expense():
    st.subheader("Delete Expense")
    response = requests.get(f"{BASE_URL}/expenses/",
                            params={"user_id": st.session_state.user_id})

    if response.status_code == 200:
        all_expenses = response.json()

        if all_expenses:
            expense_title = st.selectbox("Select Expense to Delete", [
                expense["title"] for expense in all_expenses])
            selected_expense = next(
                (expense for expense in all_expenses if expense["title"] == expense_title), None)

            if st.button(f"Delete Expense: {selected_expense["title"]}"):
                expense_id = selected_expense["id"]
                delete_route = requests.delete(
                    f"{BASE_URL}/expenses/{expense_id}")

                if delete_route.status_code == 200:
                    st.success("Expense Deleted Successfully!")
                else:
                    st.error(f"Something Went Wrong! {delete_route.text}")
        else:
            st.info("No Expenses To Delete!")
