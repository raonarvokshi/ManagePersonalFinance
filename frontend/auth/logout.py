import streamlit as st
from auth.login import login


def logout():
    st.session_state.user_authenticated = False
    st.session_state.user_id = None
    st.success("Logged out successfully!")
    login()
