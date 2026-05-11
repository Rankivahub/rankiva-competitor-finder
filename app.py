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
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 15px;
    }
    h1, h2, h3 { color: #00ff7f !important; font-family: 'Montserrat', sans-serif; text-align: center; }
    /* Table Styling */
    .stDataFrame { border: 1px solid #2e8b57; border-radius: 10px; }
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
    my_name = st.text_input("Sender Name", value="Amir Shahzad")

# --- INPUT SECTION ---
target_url = st.text_input("🌐 Enter Website URL:", placeholder="https://www.example.com")

if st.button("🚀 EXECUTE AI EXTRACTION"):
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Please provide all keys in the Sidebar.")
    else:
        with st.spinner("Creating Lead Sheet..."):
            try:
                # 1. SERPER DATA
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                biz_name = s_res.get('organic', [{}])[0].get('title', 'Business').split('-')[0].strip()
                niche = s_res.get('organic', [{}])[0].get('snippet', 'Niche').split(' ')[0]

                # 2. GEMINI AUDIT
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"SEO gaps for {target_url}. Short."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text']

                # 3. GROQ PITCH
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write luxury SEO pitch for {biz_name}. Include Subject: line. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                lines = full_text.split('\n')
                subject = next((l for l in lines if l.lower().startswith("subject:")), "Subject: Inquiry").replace("Subject:", "").strip()
                body = full_text.replace(subject, "").strip()
                email_guess = "info@" + target_url.split('//')[-1].replace('www.', '').split('/')[0]

                # --- SHEET (TABLE) CREATION ---
                st.markdown("### 📜 DATA SHEET (LEAD VIEW)")
                
                # Table ka data structure
                data = {
                    "Owner Name": ["Founding Partner"],
                    "Business Name": [biz_name],
                    "Niche": [niche],
                    "Business Mail": [email_guess],
                    "Email Subject": [subject],
                    "Mail Template": [body]
                }
                
                # Pandas DataFrame for Sheet View
                df = pd.DataFrame(data)
                
                # Displaying as a professional Table
                st.dataframe(df, use_container_width=True)

                st.success("✅ Lead Sheet is Ready!")
                
                # For Easy Copying (Bara Box niche bhi rakha hai)
                st.markdown("---")
                st.subheader("✍️ Quick Copy: Mail Template")
                st.text_area("", value=body, height=300)

            except Exception as e:
                st.error(f"Error: {str(e)}")
