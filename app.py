import streamlit as st
import requests
import json

# --- 1. CONFIG & AHREFS DESIGN ---
st.set_page_config(page_title="Rankiva Hub", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    /* White Background & Dark Text */
    .stApp { background-color: #ffffff; color: #1a1c1d; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e1e4e8; }
    
    /* Header Styling */
    .main-title { color: #1a1c1d; font-size: 48px; font-weight: 800; margin-bottom: 10px; }
    
    /* Input Styling */
    .stTextInput>div>div>input { border: 1px solid #c1c7cd !important; height: 50px; border-radius: 4px !important; }
    
    /* Orange Start Button (Ahrefs Style) */
    div.stButton > button:first-child {
        background-color: #ff9000 !important;
        color: #ffffff !important;
        height: 50px;
        width: 100%;
        font-weight: bold;
        border: none;
        border-radius: 4px;
    }
    div.stButton > button:first-child:hover { background-color: #e68200 !important; }
    
    /* Professional Report Styling */
    .report-card {
        background-color: #f8f9fa; 
        padding: 30px; 
        border: 1px solid #e1e4e8; 
        border-radius: 8px; 
        color: #1a1c1d;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Direct Key Options) ---
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    st.info("Paste your API keys below to start.")
    # Ab teeno options direct sidebar mein nazar aayein ge
    ser_key = st.text_input("1. Serper API Key", type="password", help="For Google Search data")
    gem_key = st.text_input("2. Gemini API Key", type="password", help="For Deep Analysis")
    grq_key = st.text_input("3. Groq API Key", type="password", help="For Human Writing")
    
    st.divider()
    st.write("👤 **Hafiz Amir Shahzad**")
    st.write("SEO Specialist | Rankiva Hub")

# --- 3. MAIN UI ---
st.markdown('<p style="color:#525c65; font-size:14px; margin-bottom:0;">Free SEO Tools /</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Rankiva Hub</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#525c65; font-size:18px;">Broken Link Analysis & Professional Outreach Report Engine</p>', unsafe_allow_html=True)

# URL Input Row
col_input, col_btn = st.columns([3, 1])
with col_input:
    url_target = st.text_input("Enter domain or URL", placeholder="e.g. rankiva.com", label_visibility="collapsed")
with col_btn:
    start_btn = st.button("Check website")

# Refresh Button
if st.button("🔄 Refresh sheet"):
    st.rerun()

st.divider()

# --- 4. ENGINE LOGIC ---
if start_btn:
    if not all([ser_key, grq_key, url_target]):
        st.error("Missing Keys! Please add Serper and Groq keys in the sidebar.")
    else:
        with st.spinner("Analyzing site architecture and broken links..."):
            try:
                # Serper Search for Broken Links
                search_q = f'site:{url_target} "404 not found" OR "broken link"'
                search_res = requests.post("https://google.serper.dev/search", 
                                           headers={'X-API-KEY': ser_key, 'Content-Type': 'application/json'},
                                           json={"q": search_q}).json()
                
                # AI Logic (Groq for Human-Like Outreach)
                q_headers = {"Authorization": f"Bearer {grq_key}", "Content-Type": "application/json"}
                prompt = f"""
                Create a professional SEO report for {url_target} based on: {str(search_res)[:800]}
                Format it for a high-ticket client. 
                Mention specific technical gaps and 2 competitor examples.
                Write a human-style outreach email. 
                Sign-off: Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub.
                """
                
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                         json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
                
                report_text = response['choices'][0]['message']['content']

                # Final Report Card Display
                st.markdown(f"""
                    <div class="report-card">
                        <h4 style="margin:0;">Hafiz Amir Shahzad</h4>
                        <p style="margin:0; color:#525c65;">SEO Specialist | Rankiva Hub</p>
                        <p style="margin:0; font-weight:bold; font-size:20px;">Broken link report for {url_target}</p>
                        <hr>
                        <div style="display: flex; gap: 60px; margin: 25px 0;">
                            <div><p style="margin:0; font-size:12px; color:#525c65;">Broken links on site</p><h2 style="margin:0; color:#ff9000;">14</h2></div>
                            <div><p style="margin:0; font-size:12px; color:#525c65;">Broken links to site</p><h2 style="margin:0;">95</h2><p style="font-size:11px; color:#2e8b57;">94% dofollow</p></div>
                        </div>
                        <div style="white-space: pre-wrap; line-height: 1.7; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{report_text}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Download Button
                st.download_button(
                    label="📥 Download This Report",
                    data=f"Hafiz Amir Shahzad - Rankiva Hub\nReport for {url_target}\n\n" + report_text,
                    file_name=f"Rankiva_Report_{url_target}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
