import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(
            f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            user_data = response.json()
            st.session_state.user_authenticated = True
            st.session_state.user_id = user_data["user_id"]
            st.session_state.username = user_data["username"]
            st.success("Login successful!")
            return

        else:
            st.error("Invalid username or password.")
