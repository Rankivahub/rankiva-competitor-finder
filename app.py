import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub - AI Outreach", page_icon="🌿", layout="wide")

# --- GREEN LUXURY CSS (Fixed for Streamlit New Version) ---
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
    }
    h1, h2, h3 { color: #00ff7f !important; }
    section[data-testid="stSidebar"] { background-color: #061a06; }
    .stTextArea>div>div>textarea { background-color: #0a1f0a; color: white; border: 1px solid #2e8b57; }
    </style>
    """, unsafe_allow_html=True) # <-- Yahan fix kiya gaya hai

st.title("🌿 RANKIVA HUB: ADVANCED AI OUTREACH")

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header("🔑 API DASHBOARD")
    serper_key = st.text_input("Serper API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    groq_key = st.text_input("Groq API Key", type="password")
    st.write("---")
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- INPUT SECTION ---
target_url = st.text_input("🌐 Enter Website URL to Analyze", placeholder="https://example-business.com")

if st.button("🚀 ANALYZE & GENERATE"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please provide all keys and the URL.")
    else:
        with st.spinner("Grok-Engine is extracting data..."):
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

                # 3. GROQ: Luxury Pitch
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz_name} ({target_url}). Praise them, mention gaps: {audit}. Professional easy English. Include Subject: line. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                
                full_text = gr_res['choices'][0]['message']['content']
                
                # --- UI DISPLAY ---
                st.divider()
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("🏢 Lead Details")
                    st.success(f"**Business:** {biz_name}")
                    st.markdown("**🔍 SEO Audit Summary:**")
                    st.write(audit)
                
                with col2:
                    st.subheader("📧 Outreach Content")
                    lines = full_text.split('\n')
                    subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry for " + target_url)
                    body = full_text.replace(subject, "").strip()
                    
                    st.text_input("Subject Line:", value=subject.replace("Subject:", "").strip())
                    st.text_area("Mail Template:", value=body, height=450)
                
                st.balloons()

            except Exception as e:
                st.error(f"Error: {str(e)}")
