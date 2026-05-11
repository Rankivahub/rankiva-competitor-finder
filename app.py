import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub - Lead Gen", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- GREEN LUXURY CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 1px solid #2e8b57;
        border-radius: 5px;
        height: 45px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 15px;
    }
    h1, h2, h3 { color: #00ff7f !important; font-family: 'Montserrat', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #061a06; }
    .stTextArea>div>div>textarea { background-color: #0a1f0a; color: white; border: 1px solid #2e8b57; font-size: 16px; }
    label { color: #00ff7f !important; font-weight: bold !important; margin-bottom: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 RANKIVA HUB: 6-COLUMN LEAD SYSTEM")

# --- SIDEBAR (Hidden Keys) ---
with st.sidebar:
    st.header("🔑 API CONFIG")
    serper_key = st.text_input("Serper API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    st.write("---")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- INPUT SECTION ---
target_url = st.text_input("🌐 Enter Website URL:", placeholder="https://www.example-client.com")

if st.button("🚀 EXECUTE AI EXTRACTION"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Sidebar kholen aur saari Keys enter karein!")
    else:
        with st.spinner("Finding Data & Filling Columns..."):
            try:
                # 1. SERPER DATA
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                biz_name = s_res.get('organic', [{}])[0].get('title', 'Business Owner').split('-')[0].strip()
                snippet = s_res.get('organic', [{}])[0].get('snippet', 'Services')
                niche = snippet.split(' ')[0]

                # 2. GEMINI AUDIT
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"SEO audit for {target_url}. 3 technical gaps. Very short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ PITCH
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write luxury SEO pitch for {biz_name} ({target_url}). Gaps: {audit}. Start with Subject: From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry for " + target_url)
                body = full_text.replace(subject, "").strip()

                # --- 6-COLUMN DATA DISPLAY ---
                st.markdown("### 📊 Lead Report")
                
                # Pehle 3 Columns
                row1_col1, row1_col2, row1_col3 = st.columns(3)
                with row1_col1:
                    st.text_input("1. Owner Name", value="Founding Partner", key="own")
                with row1_col2:
                    st.text_input("2. Business Name", value=biz_name, key="biz")
                with row1_col3:
                    st.text_input("3. Niche", value=niche, key="nic")

                # Agle 2 Columns
                row2_col1, row2_col2 = st.columns([1, 2])
                with row2_col1:
                    email_guess = "info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]
                    st.text_input("4. Business Mail", value=email_guess, key="mail")
                with row2_col2:
                    st.text_input("5. Email Subject", value=subject.replace("Subject:", "").strip(), key="sub")

                # Akhri Bara Column (Template)
                st.markdown("**6. Template Mail (Luxury)**")
                st.text_area("", value=body, height=350, key="templ")

                st.success("✅ Sab data columns mein fill ho gaya hai!")
                st.balloons()

            except Exception as e:
                st.error(f"Error: {str(e)}")
