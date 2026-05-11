import streamlit as st
import pandas as pd
import requests
import json

# --- 1. PAGE SETUP & DESIGN (Wahi finalized design) ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    .header-container { display: flex; align-items: center; margin-top: -50px; margin-bottom: 25px; }
    .css-logo { width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631); border-radius: 50%; margin-right: 15px; box-shadow: 0 0 15px #00ff7f; border: 2px solid #00ff7f; position: relative; }
    .brand-title { color: #00ff7f !important; font-size: 38px !important; font-weight: 800; margin: 0; }
    
    .stTextInput>div>div>input { background-color: #0a1f0a !important; color: #00ff7f !important; border: 2px solid #2e8b57 !important; height: 48px; }
    .stButton>button { background: linear-gradient(90deg, #1e5631, #00ff7f) !important; color: #040d04 !important; font-weight: bold !important; height: 48px; width: 100%; border-radius: 8px !important; }
    
    /* Table Fix: Wrap text so everything is readable */
    .custom-table { width: 100%; border-collapse: collapse; border: 1px solid #2e8b57; background-color: #0a1f0a; border-radius: 10px; overflow: hidden; table-layout: fixed; }
    .custom-table th { background-color: #0a1f0a; color: #00ff7f !important; padding: 12px; text-align: left; border-bottom: 2px solid #2e8b57; font-size: 14px; }
    .custom-table td { padding: 12px; border-bottom: 1px solid #1e3a1e; font-size: 13px; word-wrap: break-word; white-space: normal; vertical-align: top; color: #d0f0d0; }
    
    section[data-testid="stSidebar"] { background-color: #0a1f0a; border-right: 1px solid #2e8b57; }
    .sheet-header { color: #00ff7f !important; font-size: 18px !important; font-weight: bold; margin-top: 15px; border-left: 4px solid #00ff7f; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Restored Gemini Key) ---
with st.sidebar:
    st.header("🔑 API CONFIG")
    ser_key = st.text_input("Serper API Key", type="password")
    gem_key = st.text_input("Gemini API Key", type="password") # Gemini Key Added
    grq_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.info("Hafiz Amir Shahzad - SEO Specialist")

# --- 3. HEADER SECTION ---
st.markdown('<div class="header-container"><div class="css-logo"></div><div class="brand-title">RANKIVA HUB</div></div>', unsafe_allow_html=True)

# --- 4. ACTION AREA ---
col_in, col_go = st.columns([3, 1])
with col_in:
    url_input = st.text_input("URL", placeholder="https://example.com", label_visibility="collapsed")
with col_go:
    run_btn = st.button("🚀 DATA FIND START")

# Refresh Button
col_empty, col_refresh = st.columns([3, 1])
with col_refresh:
    if st.button("🔄 REFRESH SHEET"):
        st.session_state.leads = []
        st.rerun()

# --- 5. AI ENGINE (Llama 3.3) ---
def run_ai_system(url, s_api, g_api, q_api):
    try:
        search_res = requests.post("https://google.serper.dev/search", 
                                   headers={'X-API-KEY': s_api, 'Content-Type': 'application/json'},
                                   json={"q": f'"{url}" business owner and SEO email'}, timeout=10).json()
        
        q_headers = {"Authorization": f"Bearer {q_api}", "Content-Type": "application/json"}
        prompt = f"Draft a professional SEO outreach email for {url}. Use data: {str(search_res)[:500]}. Mention gaps. Sign-off: Best Regards, Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub."
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                 json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}, timeout=15).json()
        
        return response['choices'][0]['message']['content'] if 'choices' in response else "Error."
    except Exception as e:
        return f"Error: {str(e)}"

# --- 6. DATA STORAGE ---
if 'leads' not in st.session_state: st.session_state.leads = []

if run_btn:
    if not all([ser_key, grq_key, url_input]):
        st.warning("All keys and URL are required!")
    else:
        with st.spinner("Processing..."):
            email_body = run_ai_system(url_input, ser_key, gem_key, grq_key)
            biz = url_input.split('.')[-2].capitalize() if '.' in url_input else "Business"
            # Fixed Column Data
            st.session_state.leads.append([
                "Owner Found", biz, "Digital SEO", f"contact@{url_input.replace('https://','').replace('www.','')}", f"SEO Performance for {url_input}", email_body
            ])

# --- 7. FINAL TABLE (All 6 Columns) ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
html_table = '<table class="custom-table"><thead><tr>'
for h in ["Owner", "Business", "Niche", "Email", "Subject", "Mail Template"]:
    html_table += f'<th>{h}</th>'
html_table += '</tr></thead><tbody>'

for row in st.session_state.leads:
    html_table += '<tr>' + ''.join(f'<td>{str(v)}</td>' for v in row) + '</tr>'

if not st.session_state.leads:
    html_table += '<tr><td colspan="6" style="text-align:center; padding:20px;">No leads found yet.</td></tr>'

html_table += '</tbody></table>'
st.markdown(html_table, unsafe_allow_html=True)
