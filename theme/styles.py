import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #0A192F; color: white; }
        .stTextInput>div>div>input { background-color: #112240; color: white; border: 1px solid #1E3A8A; }
        .stButton>button { background-color: #3B82F6; color: white; border: none; }
        </style>
    """, unsafe_allow_html=True)
