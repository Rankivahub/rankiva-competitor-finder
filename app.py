import streamlit as st
import requests
import json

# --- 1. PAGE SETUP (Agency Design) ---
st.set_page_config(page_title="Rankiva Link Hunter", page_icon="🔗", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    .header-container { display: flex; align-items: center; margin-top: -50px; margin-bottom: 25px; }
    .css-logo { width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631); border-radius: 50%; margin-right: 15px; box-shadow: 0 0 15px #00ff7f; border: 2px solid #00ff7f; }
    .brand-title { color: #00ff7f !important; font-size: 38px !important; font-weight: 800; margin: 0; }
    .stTextInput>div>div>input { background-color: #0a1f0a !important; color: #00ff7f !important; border: 2px solid #2e8b57 !important; height: 48px; }
    .stButton>button { background: linear-gradient(90deg, #1e5631, #00ff7f) !important; color: #040d04 !important; font-weight: bold !important; height: 48px; border-radius: 8px !important; width: 100%; }
    .report-box { background-color: #0a1f0a; border: 1px solid #2e8b57; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    section[data-testid="stSidebar"] { background-color: #0a1f0a; border-right: 1px solid #2e8b57; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("🔑 SYSTEM ACCESS")
    ser_key = st.text_input("Serper API Key", type="password")
    gem_key = st.text_input("Gemini API Key", type="password")
    grq_key = st.text_input("Groq API Key", type="password")
    st.info("Hafiz Amir Shahzad - SEO Strategist")

# --- 3. HEADER ---
st.markdown('<div class="header-container"><div class="css-logo"></div><div class="brand-title">RANKIVA BROKEN LINK HUNTER</div></div>', unsafe_allow_html=True)

# --- 4. ACTION AREA ---
url_target = st.text_input("Target Domain or Keyword", placeholder="example.com or 'SEO Services London'")
col1, col2 = st.columns(2)
with col1:
    find_broken = st.button("🔍 FIND BROKEN LINKS")
with col2:
    if st.button("🔄 CLEAR"):
        st.session_state.broken_leads = []
        st.rerun()

# --- 5. BROKEN LINK ENGINE ---
def hunt_broken_links(query, s_api, q_api):
    try:
        # Serper Queries to find potentially broken pages or 404 mentions
        # Hum "inurl:404" ya "site:domain 'not found'" use kar sakte hain
        search_q = f'site:{query} "404 not found" OR "page not found" OR "broken link"'
        search_data = requests.post("https://google.serper.dev/search", 
                                   headers={'X-API-KEY': s_api, 'Content-Type': 'application/json'},
                                   json={"q": search_q}).json()
        
        q_headers = {"Authorization": f"Bearer {q_api}", "Content-Type": "application/json"}
        
        # Groq Strategy for Broken Link Outreach
        prompt = f"""
        Analyze these search results for broken links: {str(search_data)[:1000]}
        
        Task:
        1. Identify any potential broken URLs.
        2. Write a highly professional outreach email to the site owner.
        3. Logic: 
           - Tell them you were reading their site and found a broken link.
           - Politely suggest your content/service as a replacement.
           - Keep it helpful, not salesy.
        4. Sign-off: Best regards, Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub.
        """
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                 json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Hunter Error: {str(e)}"

# --- 6. OUTPUT ---
if 'broken_leads' not in st.session_state: st.session_state.broken_leads = []

if find_broken:
    if not all([ser_key, grq_key, url_target]):
        st.warning("Please enter API keys and a URL/Keyword.")
    else:
        with st.spinner("Hunting for broken links and crafting outreach..."):
            report = hunt_broken_links(url_target, ser_key, grq_key)
            st.session_state.broken_leads.append(report)

if st.session_state.broken_leads:
    for r in st.session_state.broken_leads:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.write(r)
        st.markdown('</div>', unsafe_allow_html=True)
