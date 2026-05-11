import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- GREEN LUXURY CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 2px solid #2e8b57;
        border-radius: 5px;
        height: 48px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 15px;
        font-size: 18px;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #00ff7f !important; font-family: 'Montserrat', sans-serif; text-align: center; }
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        border-radius: 10px;
        background-color: #0a1f0a;
    }
    label { color: #00ff7f !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 RANKIVA HUB: ADVANCED OUTREACH AI SYSTEM")
st.markdown("---")

# --- SIDEBAR (Keys) ---
with st.sidebar:
    st.header("🔑 API CONFIG")
    serper_key = st.text_input("Serper API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    st.write("---")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- INPUT & BUTTON SECTION (Uper wala hissa) ---
target_url = st.text_input("🌐 Enter Website URL:", placeholder="https://www.example.com")
execute_btn = st.button("🚀 EXECUTE AI EXTRACTION")

st.markdown("---")

# --- SHEET SECTION (Niche wala hissa) ---
st.markdown("### 📜 LIVE LEAD SHEET")
sheet_placeholder = st.empty()

# Default Khali Sheet
empty_data = pd.DataFrame(columns=["Owner Name", "Business Name", "Niche", "Business Mail", "Email Subject", "Mail Template"])
sheet_placeholder.dataframe(empty_data, use_container_width=True)

if execute_btn:
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please provide all keys in the Sidebar (click > top left).")
    else:
        with st.spinner("Extracting Data..."):
            try:
                # 1. SERPER DATA
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                full_title = s_res.get('organic', [{}])[0].get('title', 'Business')
                biz_name = full_title.split('-')[0].strip()
                snippet = s_res.get('organic', [{}])[0].get('snippet', 'Niche')
                niche_info = snippet.split(' ')[0].replace(',', '')

                # 2. GEMINI AUDIT
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"Quick SEO gaps for {target_url}. Very short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ PITCH
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz_name} ({target_url}). Start with Subject: line. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry").replace("Subject:", "").strip()
                body = full_text.replace(subject, "").strip()
                email_guess = "info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]

                # Update Sheet
                final_data = {
                    "Owner Name": ["Founding Partner"],
                    "Business Name": [biz_name],
                    "Niche": [niche_info],
                    "Business Mail": [email_guess],
                    "Email Subject": [subject],
                    "Mail Template": [body]
                }
                
                df_final = pd.DataFrame(final_data)
                sheet_placeholder.dataframe(df_final, use_container_width=True)

                st.success("✅ Lead Found & Added to Sheet!")
                st.balloons()
                
                # Copy Area
                st.markdown("---")
                st.subheader("✍️ Copy Mail Template")
                st.text_area("", value=body, height=300)

            except Exception as e:
                st.error(f"Error: {str(e)}")
