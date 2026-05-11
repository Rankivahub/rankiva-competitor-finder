import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- PREMIUM COMPACT CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    
    /* Rankiva Name - Left Aligned and Large */
    .brand-title {
        color: #00ff7f !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 42px !important;
        font-weight: 800;
        margin-bottom: 20px;
        margin-top: -40px;
        text-align: left;
        letter-spacing: -1px;
    }

    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 2px solid #2e8b57;
        height: 45px;
        font-size: 16px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        height: 45px;
        width: 100%;
        border: none;
        border-radius: 5px;
    }
    
    /* Table Styling */
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        background-color: #0a1f0a;
    }
    
    /* Labels and Headings */
    h3 { color: #00ff7f !important; font-size: 20px !important; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Left Aligned Big Title
st.markdown('<div class="brand-title">🌿 RANKIVA HUB</div>', unsafe_allow_html=True)

# --- SIDEBAR (Keys) ---
with st.sidebar:
    st.header("🔑 API KEYS")
    serper_key = st.text_input("Serper Key", type="password")
    gemini_key = st.text_input("Gemini Key", type="password")
    groq_key = st.text_input("Groq Key", type="password")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- COMPACT ACTION ROW ---
col_url, col_btn = st.columns([3, 1])

with col_url:
    target_url = st.text_input("URL", placeholder="https://www.example.com", label_visibility="collapsed")
with col_btn:
    execute_btn = st.button("🚀 EXECUTE")

# --- LIVE SHEET ---
st.markdown("### 📜 LIVE LEAD SHEET")
sheet_placeholder = st.empty()

# Initial Empty Sheet View
empty_df = pd.DataFrame(columns=["Owner", "Business", "Niche", "Mail", "Subject", "Template"])
sheet_placeholder.dataframe(empty_df, use_container_width=True, height=150)

if execute_btn:
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Sidebar mein keys check karein!")
    else:
        with st.spinner("Crafting Luxury Outreach..."):
            try:
                # 1. SERPER Data
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                biz = s_res.get('organic', [{}])[0].get('title', 'Business').split('-')[0].strip()
                niche = s_res.get('organic', [{}])[0].get('snippet', 'SEO').split(' ')[0]

                # 2. GROQ - Luxury Content Generation
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                # Sakht instructions for Luxury Tone
                gr_prompt = f"""Write a high-end, luxury SEO outreach email for {biz}. 
                Tone: Prestigious, elite, and professional. 
                Focus on: Bespoke digital growth and technical dominance.
                Structure: Start with 'Subject: [Luxury Subject]'. 
                From: {my_name} at Rankiva Digital."""
                
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                
                full_content = gr_res['choices'][0]['message']['content']
                
                # Parsing Subject
                lines = full_content.split('\n')
                subj = next((l for l in lines if l.lower().startswith("subject:")), "Elite Growth Opportunity").replace("Subject:", "").strip()
                
                # Final Data Prep
                final_data = {
                    "Owner": ["Founding Partner"],
                    "Business": [biz],
                    "Niche": [niche],
                    "Mail": ["info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]],
                    "Subject": [subj],
                    "Template": [full_content]
                }
                
                sheet_placeholder.dataframe(pd.DataFrame(final_data), use_container_width=True)
                st.success("✅ Luxury Lead Generated!")
                
                # Copy Area for Template
                st.markdown("---")
                st.subheader("✍️ Copy Luxury Template")
                st.text_area("", value=full_content, height=300)

            except Exception as e:
                st.error(f"Error: {str(e)}")
