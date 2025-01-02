import streamlit as st
from auth.login import login
from auth.register import register
from main import main_app

BASE_URL = "http://127.0.0.1:8000"

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_authenticated:
    st.sidebar.subheader("Authentication")
    auth_choice = st.sidebar.radio(
        "Choose an option", ["Login", "Register"])
    if auth_choice == "Login":
        login()
    elif auth_choice == "Register":
        register()
else:
    main_app()
