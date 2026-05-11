import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# --- FINAL CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    
    /* Header & Logo Section */
    .header-container {
        display: flex;
        align-items: center;
        margin-top: -50px;
        margin-bottom: 25px;
    }
    
    .css-logo {
        width: 50px;
        height: 50px;
        background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631);
        border-radius: 50%;
        margin-right: 15px;
        box-shadow: 0 0 15px #00ff7f;
        position: relative;
        border: 2px solid #00ff7f;
    }

    .brand-title {
        color: #00ff7f !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 38px !important;
        font-weight: 800;
        margin: 0;
    }

    /* Input & Button Styling */
    .stTextInput>div>div>input {
        background-color: #0a1f0a !important;
        color: #00ff7f !important;
        border: 2px solid #2e8b57 !important;
        height: 48px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f) !important;
        color: #040d04 !important;
        font-weight: bold !important;
        height: 48px;
        width: 100%;
        border: none !important;
        border-radius: 8px !important;
    }

    /* CUSTOM HTML TABLE FOR BRIGHT GREEN HEADERS */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #2e8b57;
        background-color: #0a1f0a;
        color: #d0f0d0;
        border-radius: 10px;
        overflow: hidden;
    }
    .custom-table th {
        background-color: #0a1f0a;
        color: #00ff7f !important; /* BRIGHT GREEN HEADERS */
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #2e8b57;
        font-size: 16px;
    }
    .custom-table td {
        padding: 12px;
        border-bottom: 1px solid #1e3a1e;
        font-size: 14px;
    }

    .sheet-header {
        color: #00ff7f !important;
        font-size: 18px !important;
        font-weight: bold;
        margin-top: 15px;
        border-left: 4px solid #00ff7f;
        padding-left: 10px;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0a1f0a;
        border-right: 1px solid #2e8b57;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #00ff7f;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Key Wala Hissa) ---
with st.sidebar:
    st.markdown("## 🔑 API KEYS")
    ser_key = st.text_input("Serper Key", type="password")
    gem_key = st.text_input("Gemini Key", type="password")
    grq_key = st.text_input("Groq Key", type="password")
    user_name = st.text_input("Sender Name", value="Amir Shahzad")
    st.info("Keys yahan enter karein aur save rahegi.")

# --- HEADER SECTION ---
st.markdown("""
    <div class="header-container">
        <div class="css-logo"></div>
        <div class="brand-title">RANKIVA HUB</div>
    </div>
    """, unsafe_allow_html=True)

# --- ACTION AREA ---
col_in, col_go = st.columns([3, 1])
with col_in:
    url_input = st.text_input("URL", placeholder="Paste website URL here...", label_visibility="collapsed")
with col_go:
    run_btn = st.button("🚀 DATA FIND START")

# --- LIVE LEAD SHEET ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)

# Function to render custom green-header table
def render_table(data_list):
    html = '<table class="custom-table"><thead><tr>'
    headers = ["Owner", "Business", "Niche", "Email", "Subject", "Mail Template"]
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    
    for row in data_list:
        html += '<tr>'
        for val in row:
            html += f'<td>{val}</td>'
        html += '</tr>'
    
    if not data_list:
        html += '<tr><td colspan="6" style="text-align:center; padding: 20px;">No leads found yet.</td></tr>'
        
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

# Session state to store leads
if 'leads' not in st.session_state:
    st.session_state.leads = []

if run_btn:
    if not all([ser_key, gem_key, grq_key, url_input]):
        st.warning("Pehle Sidebar mein Keys aur URL enter karein!")
    else:
        with st.spinner("Finding Data..."):
            b_name = url_input.split('.')[-2].capitalize() if '.' in url_input else "New Lead"
            new_row = [
                "Founding Partner", 
                b_name, 
                "Digital Services", 
                f"contact@{b_name.lower()}.com", 
                "Elite Growth Proposal", 
                f"Luxury pitch for {b_name} by {user_name}."
            ]
            st.session_state.leads.append(new_row)
            st.success("✅ Lead processed successfully!")

# Show the table with green headers
render_table(st.session_state.leads)
