import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub - AI Outreach", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- GREEN LUXURY CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 1px solid #2e8b57;
        border-radius: 5px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 12px;
        margin-top: 10px;
    }
    h1, h2, h3 { color: #00ff7f !important; font-family: 'Montserrat', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #061a06; }
    .stTextArea>div>div>textarea { background-color: #0a1f0a; color: white; border: 1px solid #2e8b57; }
    .stAlert { background-color: #0a1f0a; color: #00ff7f; border: 1px solid #2e8b57; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 RANKIVA HUB: SMART LEAD GENERATOR")

# --- SIDEBAR (KABHI ZARURAT HO TO SIDE SE KHOLEN) ---
with st.sidebar:
    st.header("🔑 API SETTINGS")
    serper_key = st.text_input("Serper API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    st.write("---")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- INPUT SECTION ---
target_url = st.text_input("🌐 Enter Website URL", placeholder="https://example-business.com")

if st.button("🚀 GENERATE OUTREACH"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please provide all keys in the Sidebar (click > on top left) and enter a URL.")
    else:
        with st.spinner("Rankiva AI is crafting your outreach..."):
            try:
                # 1. SERPER: Business Data
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                biz_name = s_res.get('organic', [{}])[0].get('title', 'Business Owner').split('-')[0].strip()

                # 2. GEMINI: SEO Audit
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"SEO audit for {target_url}. List 3 big technical gaps. Be brief."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ (Llama 3.3): Luxury Pitch
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz_name} ({target_url}). Praise them, mention gaps: {audit}. Use professional easy English. Include Subject: line. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                
                full_text = gr_res['choices'][0]['message']['content']
                
                # --- UI DISPLAY (AS PER YOUR REQUEST) ---
                st.divider()
                
                # Parsing Subject
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry regarding " + target_url)
                body = full_text.replace(subject, "").strip()

                # 1. Subject Box
                st.subheader("📧 Email Subject")
                st.text_input("", value=subject.replace("Subject:", "").strip(), key="subj")

                # 2. Mail Template Box
                st.subheader("✍️ Luxury Mail Template")
                st.text_area("", value=body, height=400, key="body_text")

                # 3. Business Info (Column System at bottom)
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🏢 Business Details")
                    st.info(f"**Target:** {biz_name}")
                with col2:
                    st.markdown("### 🔍 Technical Audit")
                    st.write(audit)

                st.balloons()

            except Exception as e:
                st.error(f"Error: {str(e)}")
