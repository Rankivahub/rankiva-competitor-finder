import streamlit as st
import pandas as pd
import requests
import json

# --- 1. PAGE SETUP & DESIGN ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    .header-container { display: flex; align-items: center; margin-top: -50px; margin-bottom: 25px; }
    .css-logo { width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631); border-radius: 50%; margin-right: 15px; box-shadow: 0 0 15px #00ff7f; border: 2px solid #00ff7f; position: relative; }
    .brand-title { color: #00ff7f !important; font-size: 38px !important; font-weight: 800; margin: 0; }
    
    .stTextInput>div>div>input { background-color: #0a1f0a !important; color: #00ff7f !important; border: 2px solid #2e8b57 !important; height: 48px; }
    
    /* Buttons Styling */
    .stButton>button { background: linear-gradient(90deg, #1e5631, #00ff7f) !important; color: #040d04 !important; font-weight: bold !important; height: 48px; width: 100%; border-radius: 8px !important; }
    .refresh-btn>div>button { background: #1a1a1a !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; height: 35px !important; margin-top: 10px; }

    /* Block Table Design */
    .custom-table { width: 100%; border-collapse: collapse; border: 1px solid #2e8b57; background-color: #0a1f0a; border-radius: 10px; margin-bottom: 5px; table-layout: fixed; }
    .custom-table th { background-color: #1a3a1e; color: #00ff7f !important; padding: 10px; text-align: left; border: 1px solid #2e8b57; font-size: 15px; width: 20%; }
    .custom-table td { padding: 12px; border: 1px solid #1e3a1e; font-size: 14px; word-wrap: break-word; vertical-align: top; color: #d0f0d0; }
    
    section[data-testid="stSidebar"] { background-color: #0a1f0a; border-right: 1px solid #2e8b57; }
    .sheet-header { color: #00ff7f !important; font-size: 18px !important; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-left: 4px solid #00ff7f; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("🔑 API CONFIG")
    ser_key = st.text_input("Serper API Key", type="password")
    grq_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.info("Hafiz Amir Shahzad - SEO Specialist")

# --- 3. HEADER ---
st.markdown('<div class="header-container"><div class="css-logo"></div><div class="brand-title">RANKIVA HUB</div></div>', unsafe_allow_html=True)

# --- 4. ACTION AREA ---
col_in, col_go = st.columns([3, 1])
with col_in:
    url_input = st.text_input("URL", placeholder="Paste website URL here...", label_visibility="collapsed")
with col_go:
    run_btn = st.button("🚀 DATA FIND START")

# Refresh Button exactly where it was in the image
col_empty, col_refresh = st.columns([3, 1])
with col_refresh:
    st.markdown('<div class="refresh-btn">', unsafe_allow_html=True)
    if st.button("🔄 REFRESH SHEET"):
        st.session_state.leads = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. AI ENGINE (Llama 3.3) ---
def run_ai_system(url, s_api, q_api):
    try:
        search_res = requests.post("https://google.serper.dev/search", 
                                   headers={'X-API-KEY': s_api, 'Content-Type': 'application/json'},
                                   json={"q": f'"{url}" owner business email contact'}).json()
        
        q_headers = {"Authorization": f"Bearer {q_api}", "Content-Type": "application/json"}
        prompt = f"Write a professional human-like SEO outreach email for {url} using {str(search_res)[:600]}. Greet warmly, mention 2 SEO gaps and 2 competitors. Sign-off: Best Regards, Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub."
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                 json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
        
        return response['choices'][0]['message']['content'] if 'choices' in response else "Error in generation."
    except Exception as e:
        return f"Error: {str(e)}"

# --- 6. DATA STORAGE ---
if 'leads' not in st.session_state: st.session_state.leads = []

if run_btn:
    if not all([ser_key, grq_key, url_input]):
        st.warning("Please enter all keys and URL.")
    else:
        with st.spinner("Analyzing..."):
            email_body = run_ai_system(url_input, ser_key, grq_key)
            biz = url_input.split('.')[-2].capitalize() if '.' in url_input else "Business"
            st.session_state.leads.append({
                "Owner": "Owner/Manager",
                "Business": biz,
                "Email": f"contact@{url_input.replace('https://','').replace('www.','')}",
                "Subject": f"SEO Performance Audit: {url_input}",
                "Template": email_body
            })

# --- 7. FINAL DISPLAY ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)

if st.session_state.leads:
    for i, lead in enumerate(st.session_state.leads):
        st.markdown(f"""
        <table class="custom-table">
            <tr><th>Owner Name</th><td>{lead['Owner']}</td><th>Business Name</th><td>{lead['Business']}</td></tr>
            <tr><th>Business Email</th><td colspan="3">{lead['Email']}</td></tr>
            <tr><th>Email Subject</th><td colspan="3"><b>{lead['Subject']}</b></td></tr>
            <tr><th>Mail Template</th><td colspan="3" style="white-space: pre-wrap;">{lead['Template']}</td></tr>
        </table>
        """, unsafe_allow_html=True)
        # For easy one-click copy
        st.code(lead['Template'], language="text")
        st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("No leads found yet. Enter a URL and click Start.")
