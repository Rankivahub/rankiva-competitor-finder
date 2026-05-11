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
    .stInfo { background-color: #0a1f0a; color: #00ff7f; border: 1px solid #2e8b57; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 RANKIVA HUB: 6-COLUMN LEAD SYSTEM")
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
target_url = st.text_input("🌐 Enter Website URL:", placeholder="https://www.example-client.com")

if st.button("🚀 EXECUTE AI EXTRACTION"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please fill API keys in the Sidebar and enter a URL.")
    else:
        with st.spinner("Extracting 6-Column Data..."):
            try:
                # 1. SERPER: Business Data Finding
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                
                # Logic to split data
                full_title = s_res.get('organic', [{}])[0].get('title', 'Business Owner')
                biz_name = full_title.split('-')[0].strip()
                niche = s_res.get('organic', [{}])[0].get('snippet', 'Digital Services').split(' ')[0].replace('.', '')

                # 2. GEMINI: SEO Audit & Email Finding (Simulated)
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"Quick SEO audit for {target_url}. List 3 gaps. Short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ (Llama 3.3): Luxury Pitch & Subject
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write a luxury SEO pitch for {biz_name} ({target_url}). Gaps: {audit}. Start with Subject: line. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry for " + target_url)
                body = full_text.replace(subject, "").strip()

                # --- 6-COLUMN DISPLAY LAYOUT ---
                st.markdown("### 📊 Lead Report Output")
                
                # Row 1: Business Info Columns
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**1. Owner Name**")
                    st.text_input("Owner", value="Founding Partner", label_visibility="collapsed")
                with c2:
                    st.markdown("**2. Business Name**")
                    st.text_input("Business", value=biz_name, label_visibility="collapsed")
                with c3:
                    st.markdown("**3. Niche**")
                    st.text_input("Niche", value=niche, label_visibility="collapsed")

                st.write("") # Spacer

                # Row 2: Contact & Subject
                c4, c5 = st.columns([1, 2])
                with c4:
                    st.markdown("**4. Business Mail**")
                    st.text_input("Mail", value="info@" + target_url.split('//')[-1].replace('www.', ''), label_visibility="collapsed")
                with c5:
                    st.markdown("**5. Email Subject**")
                    st.text_input("Subject", value=subject.replace("Subject:", "").strip(), label_visibility="collapsed")

                # Row 3: Template Mail
                st.markdown("**6. Template Mail (Luxury)**")
                st.text_area("Template", value=body, height=350, label_visibility="collapsed")

                # Technical Audit Info at bottom
                st.divider()
                st.info(f"**Technical Audit Gaps:** {audit}")
                st.balloons()

            except Exception as e:
                st.error(f"Error: {str(e)}")
