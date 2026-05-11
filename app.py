import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG (Keep layout wide) ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- PROFESSIONAL SLEEK CSS (Final Layout) ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    
    /* Header Container for Logo & Title alignment */
    .header-container {
        display: flex;
        align-items: center;
        margin-top: -50px; /* Pull everything up */
        margin-bottom: 20px;
        margin-left: 0px;
    }
    
    /* The New 3D Hybrid Icon */
    .brand-icon {
        width: 60px;
        height: auto;
        margin-right: 15px;
    }

    /* Rankiva Name - Large and Bold */
    .brand-title {
        color: #00ff7f !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 40px !important;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }

    /* URL Input Box styling */
    .stTextInput { margin-top: -10px !important; }
    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 2px solid #2e8b57;
        height: 45px;
        font-size: 16px;
        border-radius: 5px;
    }
    
    /* Execute Button styling */
    .stButton { margin-top: -10px !important; }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        height: 45px;
        width: 100%;
        border: none;
        border-radius: 5px;
        font-size: 16px;
    }
    
    /* Live Lead Sheet Title */
    .sheet-header {
        color: #00ff7f !important;
        font-size: 18px !important;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    /* Table/Sheet Styling */
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        border-radius: 10px;
        background-color: #0a1f0a;
    }
    
    /* Subheaders */
    h3 { color: #00ff7f !important; font-size: 18px !important; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION (Logo + Title) ---
# Raw HTML for the perfect alignment seen in the image
st.markdown(f"""
    <div class="header-container">
        <img src="https://i.imgur.com/8N4F94M.png" class="brand-icon">
        <div class="brand-title">RANKIVA HUB</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Keys hidden) ---
with st.sidebar:
    st.header("🔑 API KEYS")
    serper_key = st.text_input("Serper Key", type="password")
    gemini_key = st.text_input("Gemini Key", type="password")
    groq_key = st.text_input("Groq Key", type="password")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- ACTION ROW (Compact URL + Button) ---
col_url, col_btn = st.columns([3, 1])

with col_url:
    target_url = st.text_input("URL", placeholder="https://www.example.com", label_visibility="collapsed")
with col_btn:
    execute_btn = st.button("🚀 EXECUTE AI EXTRACTION")

# --- LIVE SHEET SECTION ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
sheet_placeholder = st.empty()

# Initial Empty Data View
empty_df = pd.DataFrame(columns=["Owner Name", "Business Name", "Niche", "Business Mail", "Email Subject", "Mail Template"])
# Set height to match the compact screen look
sheet_placeholder.dataframe(empty_df, use_container_width=True, height=200)

if execute_btn:
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please fill API keys in the Sidebar!")
    else:
        with st.spinner("Executing Elite Outreach AI..."):
            try:
                # 1. SERPER: Data Finding
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                full_title = s_res.get('organic', [{}])[0].get('title', 'Business')
                biz = full_title.split('-')[0].strip()
                snippet = s_res.get('organic', [{}])[0].get('snippet', 'SEO')
                niche_info = snippet.split(' ')[0].replace(',', '')

                # 2. GEMINI: Quick Audit (Simulated)
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"SEO gaps for {target_url}. Very short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text'][:50]

                # 3. GROQ (Llama 3.3): Luxury Content
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"""Write a high-end, luxury SEO outreach email for {biz} ({target_url}). 
                Start with 'Subject:'. Focus on elite growth. From: {my_name} at Rankiva Digital."""
                
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                
                full_content = gr_res['choices'][0]['message']['content']
                
                # Parsing Subject
                lines = full_content.split('\n')
                subj = next((l for l in lines if l.lower().startswith("subject:")), "Exclusive Opportunity").replace("Subject:", "").strip()
                
                # Business Email Guess
                email_guess = "info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]

                # Final Data Update
                final_data = {
                    "Owner Name": ["Founding Partner"],
                    "Business Name": [biz],
                    "Niche": [niche_info],
                    "Business Mail": [email_guess],
                    "Email Subject": [subj],
                    "Mail Template": [full_content]
                }
                
                # Refresh Sheet with real data
                df_final = pd.DataFrame(final_data)
                sheet_placeholder.dataframe(df_final, use_container_width=True, height=200)

                st.success("✅ Luxury Lead Data Populated!")
                st.balloons()
                
                # Separator and Copy Area
                st.markdown("---")
                st.subheader("✍️ Full Mail Template (Copy)")
                st.text_area("", value=full_content, height=350, label_visibility="collapsed")

            except Exception as e:
                st.error(f"Error: {str(e)}")
