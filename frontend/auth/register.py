import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


def register():
    st.subheader("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        response = requests.post(
            f"{BASE_URL}/auth/register", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Registration successful! Please log in.")
        else:
            st.error("Registration failed. Try a different username.")
