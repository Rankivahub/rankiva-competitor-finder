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
    }
    h1, h2, h3 { color: #00ff7f !important; font-family: 'Montserrat', sans-serif; text-align: center; }
    /* Table Styling for Sheet */
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        border-radius: 10px;
        background-color: #0a1f0a;
    }
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

# --- INPUT SECTION ---
target_url = st.text_input("🌐 Enter Website URL:", placeholder="https://www.example.com")

# Placeholder for the Sheet
st.markdown("### 📜 LIVE LEAD SHEET")
sheet_placeholder = st.empty()

# Pehle khali sheet dikhao
empty_data = pd.DataFrame(columns=["Owner Name", "Business Name", "Niche", "Business Mail", "Email Subject", "Mail Template"])
sheet_placeholder.dataframe(empty_data, use_container_width=True)

if st.button("🚀 EXECUTE AI EXTRACTION"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please provide all keys in the Sidebar (click > top left).")
    else:
        with st.spinner("Extracting Data into Sheet..."):
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
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"SEO audit for {target_url}. 3 technical gaps. Short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ PITCH
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz_name} ({target_url}). Gaps: {audit}. Start with Subject: From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry for " + target_url).replace("Subject:", "").strip()
                body = full_text.replace(subject, "").strip()
                email_guess = "info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]

                # Update Sheet with real data
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

                st.success("✅ Lead Sheet Updated Successfully!")
                st.balloons()
                
                # Copying area for Mail Template
                st.markdown("---")
                st.subheader("✍️ Quick Copy: Mail Template")
                st.text_area("", value=body, height=350)

            except Exception as e:
                st.error(f"Error: {str(e)}")
