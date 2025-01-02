import streamlit as st
import requests
import pandas as pd
from auth.logout import logout
from crud.incomes import add_income, update_income, delete_income
from crud.expenses import add_expense, update_expense, delete_expense
from report import view_report
from home import home
import os
import base64


BASE_URL = "http://127.0.0.1:8000"

current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.png")


def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def main_app():
    st.title("Personal Finance Manager 💰")
    st.markdown("---")

    if os.path.exists(logo_path):
        logo_base64 = get_image_as_base64(logo_path)
        logo_html = f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
            <img src="data:image/png;base64,{logo_base64}" style="max-width: 100%; height: auto; width: 300px;">
        </div>
        """
        with st.sidebar:
            st.markdown(logo_html, unsafe_allow_html=True)

    menu = ["Home", "Add Income", "Update Income", "Delete Income", "Add Expense",
            "Update Expense", "Delete Expense", "Financial Report", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        home()

    elif choice == "Add Income":
        add_income()

    elif choice == "Update Income":
        update_income()

    elif choice == "Delete Income":
        delete_income()

    elif choice == "Add Expense":
        add_expense()

    elif choice == "Update Expense":
        update_expense()

    elif choice == "Delete Expense":
        delete_expense()

    elif choice == "Financial Report":
        view_report()

    elif choice == "Logout":
        logout()
