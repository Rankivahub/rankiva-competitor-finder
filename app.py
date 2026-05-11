import streamlit as st
import requests
import json

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
    section[data-testid="stSidebar"] { background-color: #061a06; }
    .stTextArea>div>div>textarea { background-color: #0a1f0a; color: white; border: 1px solid #2e8b57; font-size: 16px; }
    label { color: #00ff7f !important; font-weight: bold !important; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 RANKIVA HUB: ADVANCED OUTREACH AI SYSTEM")
st.markdown("---")

# --- SIDEBAR (Hidden Keys) ---
with st.sidebar:
    st.header("🔑 API CONFIG")
    serper_key = st.text_input("Serper API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    st.write("---")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- INPUT SECTION ---
target_url = st.text_input("🌐 Enter Website URL:", placeholder="https://www.client-website.com")

if st.button("🚀 EXECUTE AI EXTRACTION"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please provide all API keys in the Sidebar (click > top left).")
    else:
        with st.spinner("Rankiva AI is Analyzing..."):
            try:
                # 1. SERPER DATA
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                full_title = s_res.get('organic', [{}])[0].get('title', 'Business Owner')
                biz_name = full_title.split('-')[0].strip()
                snippet = s_res.get('organic', [{}])[0].get('snippet', 'Digital Services')
                niche = snippet.split(' ')[0].replace(',', '')

                # 2. GEMINI AUDIT
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"Quick SEO audit for {target_url}. List 3 technical gaps. Very short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ PITCH
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz_name} ({target_url}). Gaps: {audit}. Start with Subject: line. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                # Parsing Subject and Body
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry for " + target_url)
                body = full_text.replace(subject, "").strip()

                # --- 6-COLUMN DATA FILLING ---
                st.markdown("### 📊 Extracted Lead Data")
                
                # Row 1: Basic Info
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.text_input("1. Owner Name", value="Founding Partner")
                with c2:
                    st.text_input("2. Business Name", value=biz_name)
                with c3:
                    st.text_input("3. Niche", value=niche)

                # Row 2: Mail & Subject
                c4, c5 = st.columns([1, 2])
                with c4:
                    email_guess = "info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]
                    st.text_input("4. Business Mail", value=email_guess)
                with c5:
                    st.text_input("5. Email Subject", value=subject.replace("Subject:", "").strip())

                # Row 3: Template Mail (Full Width)
                st.markdown("**6. Luxury Mail Template**")
                st.text_area("", value=body, height=350)

                st.success("✅ Analysis Complete! All data filled below.")
                st.balloons()

            except Exception as e:
                st.error(f"Error: {str(e)}")
