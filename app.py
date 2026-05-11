import streamlit as st
import requests
import json

# --- 1. PAGE SETUP & THEME (Rankiva Branding) ---
st.set_page_config(page_title="Rankiva Agency AI", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #040d04; color: #d0f0d0; }
    .header-container { display: flex; align-items: center; margin-top: -50px; margin-bottom: 25px; }
    .css-logo { width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #57ff91, #1e5631); border-radius: 50%; margin-right: 15px; box-shadow: 0 0 15px #00ff7f; border: 2px solid #00ff7f; }
    .brand-title { color: #00ff7f !important; font-size: 38px !important; font-weight: 800; margin: 0; }
    
    .stTextInput>div>div>input { background-color: #0a1f0a !important; color: #00ff7f !important; border: 2px solid #2e8b57 !important; height: 48px; }
    .stButton>button { background: linear-gradient(90deg, #1e5631, #00ff7f) !important; color: #040d04 !important; font-weight: bold !important; height: 48px; border-radius: 8px !important; width: 100%; }
    
    /* Agency Table Display */
    .agency-table { width: 100%; border-collapse: collapse; border: 1px solid #2e8b57; background-color: #0a1f0a; border-radius: 12px; overflow: hidden; margin-bottom: 30px; }
    .agency-table th { background-color: #1a3a1e; color: #00ff7f !important; padding: 15px; text-align: left; border: 1px solid #2e8b57; font-size: 15px; width: 25%; }
    .agency-table td { padding: 15px; border: 1px solid #1e3a1e; font-size: 14px; vertical-align: top; color: #d0f0d0; line-height: 1.6; }
    
    section[data-testid="stSidebar"] { background-color: #0a1f0a; border-right: 1px solid #2e8b57; }
    .section-label { color: #00ff7f !important; font-size: 20px !important; font-weight: bold; margin-bottom: 15px; padding-left: 10px; border-left: 5px solid #00ff7f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR CONFIG ---
with st.sidebar:
    st.header("🔑 SYSTEM ACCESS")
    ser_key = st.text_input("Serper API Key", type="password")
    gem_key = st.text_input("Gemini API Key", type="password")
    grq_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.info("Hafiz Amir Shahzad\nSenior SEO Specialist\nRankiva Hub")

# --- 3. BRANDING ---
st.markdown('<div class="header-container"><div class="css-logo"></div><div class="brand-title">RANKIVA AGENCY ENGINE</div></div>', unsafe_allow_html=True)

# --- 4. INPUT SECTION ---
col_url, col_btn = st.columns([3, 1])
with col_url:
    url_target = st.text_input("Analysis URL", placeholder="Paste website link here...", label_visibility="collapsed")
with col_btn:
    start_btn = st.button("🚀 START STRATEGIC ANALYSIS")

if st.button("🔄 CLEAR DATA"):
    st.session_state.agency_leads = []
    st.rerun()

# --- 5. THE STRATEGIST ENGINE ---
def run_agency_analysis(url, s_api, g_api, q_api):
    try:
        # Step 1: Deep Search using Serper
        search_q = f'"{url}" business owner, contact email, top 2 organic competitors, niche services'
        search_data = requests.post("https://google.serper.dev/search", 
                                   headers={'X-API-KEY': s_api, 'Content-Type': 'application/json'},
                                   json={"q": search_q}).json()
        
        # Step 2: Advanced Brain (Groq with Llama 3.3 for Human Writing)
        q_headers = {"Authorization": f"Bearer {q_api}", "Content-Type": "application/json"}
        
        prompt = f"""
        Act as a Senior SEO Outreach Strategist. 
        Analyze the following data for {url}: {str(search_data)[:1000]}
        
        Follow these steps strictly:
        1. Extract: Business Name, Owner (if any), Niche, Location, and Business Email.
        2. Identify 2 Competitors and their SEO advantage over {url}.
        3. Identify 3 critical SEO Gaps (e.g. missing high-intent pages, weak conversion, topical authority).
        4. Write ONE highly personalized email:
           - Start with asking about their well-being.
           - Compliment their specific work or site messaging.
           - Mention 2 specific observations about their site.
           - Naturally bridge into SEO gaps using competitor examples.
           - Tone: Human consultant, calm, NO marketing hype, simple English.
           - NO buzzwords like 'game changer' or 'unlock'.
        
        Sign-off: 
        Best regards, 
        Hafiz Amir Shahzad 
        SEO Specialist 
        Rankiva hub
        """
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                 json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
        
        final_report = response['choices'][0]['message']['content']
        return final_report
    except Exception as e:
        return f"System Error: {str(e)}"

# --- 6. OUTPUT & DISPLAY ---
if 'agency_leads' not in st.session_state: st.session_state.agency_leads = []

if start_btn:
    if not all([ser_key, gem_key, grq_key, url_target]):
        st.warning("Please configure all API keys in the sidebar.")
    else:
        with st.spinner("Analyzing Business, Gaps, and Competitors..."):
            report = run_agency_analysis(url_target, ser_key, gem_key, grq_key)
            st.session_state.agency_leads.append({"url": url_target, "report": report})

st.markdown('<div class="section-label">📜 STRATEGIC REPORTS</div>', unsafe_allow_html=True)

if st.session_state.agency_leads:
    for item in st.session_state.agency_leads:
        with st.container():
            st.markdown(f"### Analysis for: {item['url']}")
            # Text area with high height for full readability
            st.text_area("Full Agency Report (Analysis + Email)", value=item['report'], height=600)
            st.markdown("---")
else:
    st.info("No research data found. Start by entering a URL.")
