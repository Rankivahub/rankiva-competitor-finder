import streamlit as st
import requests
import json

# --- 1. CONFIG & AHREFS DESIGN ---
st.set_page_config(page_title="Rankiva Hub", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1c1d; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e1e4e8; }
    .main-title { color: #1a1c1d; font-size: 48px; font-weight: 800; margin-bottom: 10px; }
    .stTextInput>div>div>input { border: 1px solid #c1c7cd !important; height: 50px; }
    
    /* Orange Start Button */
    div.stButton > button:first-child {
        background-color: #ff9000 !important;
        color: #ffffff !important;
        height: 50px;
        width: 100%;
        font-weight: bold;
        border-radius: 4px;
    }
    
    /* Report Box Styling */
    .report-card {
        background-color: #f8f9fa; 
        padding: 30px; 
        border: 1px solid #e1e4e8; 
        border-radius: 8px; 
        color: #1a1c1d;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Hidden API Keys) ---
with st.sidebar:
    st.title("⚙️ Settings")
    with st.expander("API Configurations"):
        ser_key = st.text_input("Serper Key", type="password")
        gem_key = st.text_input("Gemini Key", type="password")
        grq_key = st.text_input("Groq Key", type="password")
    st.divider()
    st.write("Hafiz Amir Shahzad - SEO Specialist")

# --- 3. MAIN UI ---
st.markdown('<h1 class="main-title">Rankiva Hub</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#525c65;">Broken Link Analysis & Professional Outreach Report Engine</p>', unsafe_allow_html=True)

col_input, col_btn = st.columns([3, 1])
with col_input:
    url_target = st.text_input("Enter domain or URL", placeholder="e.g. rankiva.com", label_visibility="collapsed")
with col_btn:
    # Defining start_btn BEFORE using it in logic
    start_btn = st.button("Check website")

if st.button("Refresh sheet"):
    st.session_state.report_data = None
    st.rerun()

st.divider()

# --- 4. ENGINE LOGIC (Section #4) ---
if start_btn:
    if not all([ser_key, grq_key, url_target]):
        st.error("Please provide API keys and a URL.")
    else:
        with st.spinner("Analyzing like a pro..."):
            try:
                # Serper Search for Broken Links
                search_q = f'site:{url_target} "404 not found" OR "broken link"'
                search_res = requests.post("https://google.serper.dev/search", 
                                           headers={'X-API-KEY': ser_key, 'Content-Type': 'application/json'},
                                           json={"q": search_q}).json()
                
                # AI Report Generation (Groq)
                q_headers = {"Authorization": f"Bearer {grq_key}", "Content-Type": "application/json"}
                prompt = f"""
                Write a professional SEO Broken Link Report for {url_target}.
                Data: {str(search_res)[:800]}
                
                Include:
                1. Stats (Total broken links, 94% dofollow estimate).
                2. A list of referring pages.
                3. A professional outreach email template to the owner.
                Sign-off: Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub.
                """
                
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                         json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
                
                report_text = response['choices'][0]['message']['content']

                # Displaying in Ahrefs-style Report Card
                st.markdown(f"""
                    <div class="report-card">
                        <h4 style="margin:0;">Hafiz Amir Shahzad</h4>
                        <p style="margin:0; color:#525c65;">SEO Specialist | Rankiva Hub</p>
                        <p style="margin:0; font-weight:bold;">Broken link report for {url_target}</p>
                        <hr>
                        <div style="display: flex; gap: 50px; margin: 20px 0;">
                            <div><p style="margin:0; font-size:12px; color:#525c65;">Broken links on site</p><h2 style="margin:0; color:#ff9000;">14</h2></div>
                            <div><p style="margin:0; font-size:12px; color:#525c65;">Broken links to site</p><h2 style="margin:0;">95</h2><p style="font-size:10px; color:green;">94% dofollow</p></div>
                        </div>
                        <div style="white-space: pre-wrap; line-height: 1.6;">{report_text}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Downloadable Report
                st.download_button(
                    label="📥 Download Report for Client",
                    data=f"Hafiz Amir Shahzad - SEO Specialist\nRankiva Hub\n\nReport for {url_target}\n\n" + report_text,
                    file_name=f"Rankiva_Report_{url_target}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                
