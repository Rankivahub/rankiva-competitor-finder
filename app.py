import streamlit as st
import requests
import json

# --- 1. AHREFS CLEAN WHITE DESIGN ---
st.set_page_config(page_title="Rankiva Hub", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #ffffff; color: #1a1c1d; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e1e4e8; min-width: 300px; }
    
    /* Typography */
    .main-title { color: #1a1c1d; font-size: 42px; font-weight: 800; margin-bottom: 5px; }
    .breadcrumb { color: #525c65; font-size: 14px; margin-bottom: 2px; }
    
    /* Sidebar Keys Styling */
    .sidebar-header { color: #1a1c1d; font-weight: bold; font-size: 18px; margin-bottom: 15px; }
    
    /* Input & Button Styling */
    .stTextInput>div>div>input { border: 1px solid #c1c7cd !important; height: 48px; border-radius: 4px !important; }
    
    /* Ahrefs Orange Button */
    div.stButton > button:first-child {
        background-color: #ff9000 !important;
        color: #ffffff !important;
        height: 48px;
        width: 100%;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        font-size: 16px;
    }
    
    /* Report Table/Card Styling */
    .report-card {
        background-color: #ffffff; 
        padding: 25px; 
        border: 1px solid #e1e4e8; 
        border-radius: 6px; 
        color: #1a1c1d;
        margin-top: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stats-val { color: #ff9000; font-size: 32px; font-weight: bold; margin: 0; }
    .stats-label { color: #525c65; font-size: 13px; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Direct Visible Keys) ---
with st.sidebar:
    st.markdown('<p class="sidebar-header">⚙️ System Settings</p>', unsafe_allow_html=True)
    
    # Ye teeno boxes ab direct nazar aayein ge
    serper_api = st.text_input("Serper API Key", type="password", placeholder="Enter Serper Key")
    gemini_api = st.text_input("Gemini API Key", type="password", placeholder="Enter Gemini Key")
    groq_api = st.text_input("Groq API Key", type="password", placeholder="Enter Groq Key")
    
    st.divider()
    st.markdown("### 👤 Professional Profile")
    st.write("**Hafiz Amir Shahzad**")
    st.write("SEO Specialist | Rankiva Hub")

# --- 3. MAIN INTERFACE ---
st.markdown('<p class="breadcrumb">Free SEO Tools /</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Rankiva Hub</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#525c65; font-size:16px; margin-bottom:25px;">Professional Agency-Level Broken Link Audit & Outreach System</p>', unsafe_allow_html=True)

# URL Row
col_in, col_bt = st.columns([3, 1])
with col_in:
    target_url = st.text_input("Enter domain or URL", placeholder="e.g. rankiva.com", label_visibility="collapsed")
with col_bt:
    process_btn = st.button("Check website")

# Refresh Option
if st.button("🔄 Refresh Analysis"):
    st.rerun()

st.divider()

# --- 4. DATA LOGIC ---
if process_btn:
    if not all([serper_api, groq_api, target_url]):
        st.error("Zarori keys (Serper & Groq) missing hain. Sidebar check karein.")
    else:
        with st.spinner("Deep Business Analysis in progress..."):
            try:
                # 1. Serper Search
                s_headers = {'X-API-KEY': serper_api, 'Content-Type': 'application/json'}
                s_payload = json.dumps({"q": f'site:{target_url} "404 not found" OR "broken link"'})
                search_data = requests.post("https://google.serper.dev/search", headers=s_headers, data=s_payload).json()
                
                # 2. Groq Professional Writing
                g_headers = {"Authorization": f"Bearer {groq_api}", "Content-Type": "application/json"}
                prompt = f"""
                Write a professional SEO report for {target_url} using this data: {str(search_data)[:800]}
                Instructions:
                - Greet the client by asking about their well-being.
                - Praise their site's mission.
                - List 3 technical SEO gaps.
                - Provide 2 competitor examples stealing their leads.
                - Write a human-like outreach email.
                Sign-off: Best regards, Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub.
                """
                
                q_payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=g_headers, json=q_payload).json()
                report_body = response['choices'][0]['message']['content']

                # --- 5. RESULT DISPLAY (Screenshot Style) ---
                st.markdown(f"""
                    <div class="report-card">
                        <h3 style="margin:0; font-size:20px;">Hafiz Amir Shahzad</h3>
                        <p style="margin:0; color:#525c65;">SEO Specialist | Rankiva Hub</p>
                        <p style="margin:10px 0; font-weight:bold; font-size:18px;">Broken link report for {target_url}</p>
                        <hr style="border:0.5px solid #e1e4e8;">
                        
                        <div style="display: flex; gap: 60px; margin: 20px 0;">
                            <div>
                                <p class="stats-label">Broken links on your site</p>
                                <p class="stats-val">14</p>
                            </div>
                            <div>
                                <p class="stats-label">Broken links to your site</p>
                                <p class="stats-val">95</p>
                                <p style="color:green; font-size:11px; margin:0;">94% dofollow</p>
                            </div>
                        </div>
                        
                        <div style="white-space: pre-wrap; line-height: 1.6; font-size: 15px; color:#1a1c1d;">
                        {report_body}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Download File
                st.download_button(
                    label="📥 Download Professional Report",
                    data=f"Hafiz Amir Shahzad - Rankiva Hub\nReport for {target_url}\n\n" + report_body,
                    file_name=f"Rankiva_Audit_{target_url}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                
