import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- FINAL COMPACT CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    
    /* Header Container for Logo & Title alignment */
    .header-container {
        display: flex;
        align-items: center;
        margin-top: -60px; /* Pull everything up */
        margin-bottom: 15px;
        margin-left: 0px;
    }
    
    /* The New Green Sphere Logo */
    .brand-icon {
        width: 65px; /* Adjusting size to match Rankiva Hub text */
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
    }
    
    /* Table/Sheet Styling */
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        border-radius: 10px;
        background-color: #0a1f0a;
    }

    .sheet-header {
        color: #00ff7f !important;
        font-size: 18px !important;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION (New Sphere Logo + Title) ---
st.markdown(f"""
    <div class="header-container">
        <img src="https://i.ibb.co/v4S8F1H/green-sphere-logo.png" class="brand-icon">
        <div class="brand-title">RANKIVA HUB</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Hidden Keys) ---
with st.sidebar:
    st.header("🔑 API CONFIG")
    serper_key = st.text_input("Serper Key", type="password")
    gemini_key = st.text_input("Gemini Key", type="password")
    groq_key = st.text_input("Groq Key", type="password")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- ACTION ROW ---
col_url, col_btn = st.columns([3, 1])

with col_url:
    target_url = st.text_input("URL", placeholder="https://www.example.com", label_visibility="collapsed")
with col_btn:
    execute_btn = st.button("🚀 EXECUTE")

# --- LIVE SHEET SECTION ---
st.markdown('<div class="sheet-header">📜 LIVE LEAD SHEET</div>', unsafe_allow_html=True)
sheet_placeholder = st.empty()

# Initial View
empty_df = pd.DataFrame(columns=["Owner Name", "Business Name", "Niche", "Business Mail", "Email Subject", "Mail Template"])
sheet_placeholder.dataframe(empty_df, use_container_width=True, height=200)

if execute_btn:
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please fill all keys in Sidebar!")
    else:
        with st.spinner("Analyzing..."):
            try:
                # 1. SERPER DATA
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                biz = s_res.get('organic', [{}])[0].get('title', 'Business').split('-')[0].strip()
                snippet = s_res.get('organic', [{}])[0].get('snippet', 'Digital')
                niche = snippet.split(' ')[0]

                # 2. GROQ LUXURY PITCH
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz} ({target_url}). From: {my_name} at Rankiva Digital."
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                # Update Sheet
                final_data = {
                    "Owner Name": ["Founding Partner"],
                    "Business Name": [biz],
                    "Niche": [niche],
                    "Business Mail": ["info@" + target_url.split('//')[-1].replace('www.', '')],
                    "Email Subject": ["Elite Growth Proposal"],
                    "Mail Template": [full_text]
                }
                sheet_placeholder.dataframe(pd.DataFrame(final_data), use_container_width=True, height=200)
                st.success("✅ Lead Generated!")
                
                # Copy Area
                st.text_area("Full Template Copy:", value=full_text, height=300)

            except Exception as e:
                st.error(f"Error: {str(e)}")
