import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


def add_income():
    st.subheader("Add Income")
    title = st.text_input("Title")
    amount = st.number_input("Income Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description")

    if st.button("Add Income"):
        if not title or not amount and not description:
            st.error("Please fill out all the required fields!")

        elif title and description and amount == 0.0:
            st.error("Amount can not be 0")

        elif title and amount and description:
            if amount == 0:
                st.error("Amount can not be 0")
            else:
                json = {
                    "user_id": st.session_state.user_id,
                    "title": title,
                    "amount": amount,
                    "description": description,
                }

                response = requests.post(
                    f"{BASE_URL}/incomes/",
                    json=json
                )

                if response.status_code == 200:
                    st.success("Income added successfully!")

                else:
                    st.error(f"Failed to add income. Error: {response.text}")


def update_income():
    st.subheader("Update Income")

    response = requests.get(f"{BASE_URL}/incomes/",
                            params={"user_id": st.session_state.user_id})
    if response.status_code == 200:
        all_incomes = response.json()
        if all_incomes:
            income_title = st.selectbox("Select Income to Update", [
                income["title"] for income in all_incomes])
            st.markdown("---")
            selected_income = next(
                (income for income in all_incomes if income["title"] == income_title), None)

            if selected_income:
                new_title = st.text_input(
                    "New Title", value=selected_income["title"])
                new_amount = st.number_input(
                    "New Amount", value=selected_income["amount"], min_value=0.0, step=0.01)
                new_description = st.text_area(
                    "New Description", value=selected_income["description"])
                new_date = st.date_input("New Date", value=pd.to_datetime(
                    selected_income["date"]).date())

                if st.button("Update Income"):
                    json = {
                        "title": new_title,
                        "amount": new_amount,
                        "description": new_description,
                        "date": new_date.isoformat(),
                    }

                    update_response = requests.put(
                        f"{BASE_URL}/incomes/{selected_income["id"]}",
                        json=json
                    )

                    if update_response.status_code == 200:
                        st.success("Income updated successfully!")

                    else:
                        st.error(
                            f"Failed to update income! Error: {update_response.text}")
        else:
            st.info("No Incomes Found To Update!")
    else:
        st.error(f"Failed to fetch incomes. Error: {response.text}")


def delete_income():
    st.subheader("Delete Income")
    response = requests.get(f"{BASE_URL}/incomes/",
                            params={"user_id": st.session_state.user_id})

    if response.status_code == 200:
        all_incomes = response.json()
        if all_incomes:
            income_title = st.selectbox("Select Income to Delete", [
                income["title"] for income in all_incomes])
            selected_income = next(
                (income for income in all_incomes if income["title"] == income_title), None)

            if st.button(f"Delete Income:  {selected_income["title"]}"):
                income_id = selected_income["id"]
                delete_route = requests.delete(
                    f"{BASE_URL}/incomes/{income_id}")
                if delete_route.status_code == 200:
                    st.success("Income Deleted Successfully!")
                else:
                    st.error(f"Something went wrong! {delete_route.text}")
        else:
            st.info("No Incomes Found To delete!")
