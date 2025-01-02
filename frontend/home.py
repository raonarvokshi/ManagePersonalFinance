import streamlit as st
import requests
import pandas as pd


BASE_URL = "http://127.0.0.1:8000"


def home():
    st.subheader(f"Welcome, {st.session_state.username.capitalize()}!")
    st.write("***Use this application to manage your monthly income and expenses.***")
    st.markdown("---")

    expenses_response = requests.get(
        f"{BASE_URL}/expenses/", params={"user_id": st.session_state.user_id})

    incomes_response = requests.get(
        f"{BASE_URL}/incomes/", params={"user_id": st.session_state.user_id})

    if expenses_response.status_code == 200 and incomes_response.status_code == 200:
        expenses = expenses_response.json()
        incomes = incomes_response.json()

        expenses_df = pd.DataFrame(expenses)
        incomes_df = pd.DataFrame(incomes)

        if "date" in expenses_df.columns:
            expenses_df["date"] = pd.to_datetime(
                expenses_df["date"], format="mixed").dt.date
            expenses_df = expenses_df.sort_values(by="date")

        if "date" in incomes_df.columns:
            incomes_df["date"] = pd.to_datetime(
                incomes_df["date"], format="mixed").dt.date
            incomes_df = incomes_df.sort_values(by="date")

        if incomes_df.empty and expenses_df.empty:
            st.warning("No data available to generate the dataframes")
            st.info("Please start by adding new incomes and expenses")
        else:
            if incomes_df.empty:
                st.warning(
                    "No Incomes data available to generate the dataframe")
                st.info("Please start by adding new incomes")
            else:
                st.write("### Incomes 💲")
                if "id" in incomes_df.columns and "user_id" in incomes_df.columns:
                    incomes_df = incomes_df.drop(columns=["id", "user_id"])
                incomes_df.reset_index(drop=True, inplace=True)
                st.dataframe(incomes_df, use_container_width=True,
                             hide_index=True)

            if expenses_df.empty:
                st.warning(
                    "No Expenses data available to generate the dataframe!")
                st.info("Please start by adding new expenses.")
            else:
                st.write("### Expenses 💳")
                if "id" in expenses_df.columns and "user_id" in expenses_df.columns:
                    expenses_df = expenses_df.drop(columns=["id", "user_id"])
                expenses_df.reset_index(drop=True, inplace=True)
                st.dataframe(expenses_df, use_container_width=True,
                             hide_index=True)

    else:
        if not expenses_response.status_code != 200:
            st.error(
                f"Failed to retreive expenses data! {expenses_response.text}")

        if not incomes_response.status_code != 200:
            st.error(
                f"Failed to retreive incomes data! {incomes_response.text}")
