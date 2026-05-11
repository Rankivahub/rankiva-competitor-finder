import streamlit as st
import pandas as pd
import requests
import json

# --- 1. PAGE SETUP & DESIGN (Full Visibility Fix) ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    .header-container { display: flex; align-items: center; margin-top: -50px; margin-bottom: 25px; }
    .css-logo { width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631); border-radius: 50%; margin-right: 15px; box-shadow: 0 0 15px #00ff7f; border: 2px solid #00ff7f; position: relative; }
    .brand-title { color: #00ff7f !important; font-size: 38px !important; font-weight: 800; margin: 0; }
    
    /* Input & Buttons */
    .stTextInput>div>div>input { background-color: #0a1f0a !important; color: #00ff7f !important; border: 2px solid #2e8b57 !important; height: 48px; }
    .stButton>button { background: linear-gradient(90deg, #1e5631, #00ff7f) !important; color: #040d04 !important; font-weight: bold !important; height: 48px; width: 100%; border-radius: 8px !important; }
    
    /* Table Fix: Wrap text so it shows completely */
    .custom-table { width: 100%; border-collapse: collapse; border: 1px solid #2e8b57; background-color: #0a1f0a; border-radius: 10px; table-layout: fixed; }
    .custom-table th { background-color: #0a1f0a; color: #00ff7f !important; padding: 12px; text-align: left; border-bottom: 2px solid #2e8b57; font-size: 16px; }
    .custom-table td { padding: 12px; border-bottom: 1px solid #1e3a1e; font-size: 14px; word-wrap: break-word; white-space: normal; vertical-align: top; }
    
    section[data-testid="stSidebar"] { background-color: #0a1f0a; border-right: 1px solid #2e8b57; }
    .sheet-header { color: #00ff7f !important; font-size: 18px !important; font-weight: bold; margin-top: 15px; border-left: 4px solid #00ff7f; padding-left: 10px; }
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
    url_input = st.text_input("URL", placeholder="https://example.com", label_visibility="collapsed")
with col_go:
    run_btn = st.button("🚀 DATA FIND START")

# --- 5. IMPROVED AI ENGINE ---
def run_ai_system(url, s_api, q_api):
    try:
        # Step 1: Deep Search for REAL Email & Owner
        search_q = f'"{url}" owner business email contact "@{".".join(url.split(".")[-2:])}"'
        search_res = requests.post("https://google.serper.dev/search", 
                                   headers={'X-API-KEY': s_api, 'Content-Type': 'application/json'},
                                   json={"q": search_q}, timeout=10).json()
        
        # Step 2: Groq for Unique Human Outreach
        q_headers = {"Authorization": f"Bearer {q_api}", "Content-Type": "application/json"}
        prompt = f"Analyze website {url} and search results {str(search_res)[:800]}. Write a professional, friendly SEO outreach email. Include 2 specific gaps and mention competitors are leading. Sign-off: Best Regards, Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub."
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                 json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}, timeout=15)
        res_json = response.json()
        
        email_content = res_json['choices'][0]['message']['content'] if 'choices' in res_json else "Error generating email."
        return email_content
    except Exception as e:
        return f"Error: {str(e)}"

# --- 6. DATA STORAGE ---
if 'leads' not in st.session_state: st.session_state.leads = []

if run_btn:
    if not all([ser_key, grq_key, url_input]):
        st.warning("Keys aur URL enter karein!")
    else:
        with st.spinner("Finding Real Data & Drafting Email..."):
            email_body = run_ai_system(url_input, ser_key, grq_key)
            biz = url_input.split('.')[-2].capitalize() if '.' in url_input else "Business"
            st.session_state.leads.append({
                "Owner": "Owner/Manager",
                "Business": biz,
                "Niche": "Digital/SEO",
                "Email": f"contact@{url_input.replace('https://','').replace('www.','')}",
                "Subject": f"Re: {url_input} - Performance Audit & Strategy",
                "Template": email_body
            })

# --- 7. FINAL DISPLAY & REFRESH ---
col_head, col_ref = st.columns([5, 1])
with col_head:
    st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
with col_ref:
    if st.button("🔄 REFRESH"):
        st.session_state.leads = []
        st.rerun()

# Render Table with Full Text Visibility
if st.session_state.leads:
    for i, lead in enumerate(st.session_state.leads):
        with st.container():
            st.markdown(f"""
            <table class="custom-table">
                <tr><th>Owner</th><th>Business</th><th>Niche</th><th>Email</th></tr>
                <tr><td>{lead['Owner']}</td><td>{lead['Business']}</td><td>{lead['Niche']}</td><td>{lead['Email']}</td></tr>
                <tr><th colspan="4">Subject</th></tr>
                <tr><td colspan="4">{lead['Subject']}</td></tr>
                <tr><th colspan="4">Mail Template</th></tr>
                <tr><td colspan="4" style="white-space: pre-wrap;">{lead['Template']}</td></tr>
            </table>
            """, unsafe_allow_html=True)
            # Simple copy button for each lead
            st.button(f"📋 Copy Mail {i+1}", on_click=lambda t=lead['Template']: st.write(f"Copy this: \n\n {t}"), key=f"btn_{i}")
            st.markdown("<br>", unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align:center; padding:20px; background:#0a1f0a; border-radius:10px;">No leads found yet.</div>', unsafe_allow_html=True)
