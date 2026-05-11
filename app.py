import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rankiva Hub AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# --- COMPACT LUXURY CSS ---
st.markdown("""
    <style>
    .main { background-color: #040d04; color: #d0f0d0; }
    /* Heading Spacing kam karne ke liye */
    h1 { color: #00ff7f !important; margin-top: -50px !important; font-size: 28px !important; text-align: center; }
    .stTextInput { margin-top: -20px !important; }
    .stButton { margin-top: -10px !important; }
    
    .stTextInput>div>div>input {
        background-color: #0a1f0a;
        color: #00ff7f;
        border: 2px solid #2e8b57;
        height: 40px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e5631, #00ff7f);
        color: #040d04;
        font-weight: bold;
        height: 45px;
        width: 100%;
    }
    /* Sheet Design */
    [data-testid="stDataFrame"] {
        border: 2px solid #2e8b57;
        background-color: #0a1f0a;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 RANKIVA HUB: ADVANCED OUTREACH AI SYSTEM")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 KEYS")
    serper_key = st.text_input("Serper Key", type="password")
    gemini_key = st.text_input("Gemini Key", type="password")
    groq_key = st.text_input("Groq Key", type="password")
    my_name = st.text_input("Sender", value="Amir Shahzad")

# --- COMPACT LAYOUT ---
# Ek hi line mein URL aur Button taake jagah bache
col_url, col_btn = st.columns([3, 1])

with col_url:
    target_url = st.text_input("Website URL:", placeholder="example.com", label_visibility="collapsed")
with col_btn:
    execute_btn = st.button("🚀 EXECUTE")

# LIVE SHEET (Uper hi nazar aayegi)
st.markdown("<h3 style='font-size: 18px; color: #00ff7f;'>📜 LIVE LEAD SHEET</h3>", unsafe_allow_html=True)
sheet_placeholder = st.empty()

# Default Khali Data
empty_df = pd.DataFrame(columns=["Owner", "Business", "Niche", "Mail", "Subject", "Template"])
sheet_placeholder.dataframe(empty_df, use_container_width=True, height=150)

if execute_btn:
    if not all([serper_key, gemini_key, groq_key, target_url]):
        st.error("Keys missing in Sidebar!")
    else:
        with st.spinner("Finding Lead..."):
            try:
                # 1. SERPER
                s_res = requests.post("https://google.serper.dev/search", 
                                     headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                                     data=json.dumps({"q": target_url})).json()
                biz = s_res.get('organic', [{}])[0].get('title', 'Business').split('-')[0].strip()
                niche = s_res.get('organic', [{}])[0].get('snippet', 'SEO').split(' ')[0]

                # 2. GEMINI (Audit)
                g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": f"SEO gaps for {target_url}."}]}]}).json()
                audit = g_res['candidates'][0]['content']['parts'][0]['text'][:50]

                # 3. GROQ (Pitch)
                gr_url = "https://api.groq.com/openai/v1/chat/completions"
                gr_prompt = f"Write luxury pitch for {biz}. Include Subject. From: {my_name}"
                gr_res = requests.post(gr_url, 
                                     headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": gr_prompt}]}).json()
                full_text = gr_res['choices'][0]['message']['content']
                
                lines = full_text.split('\n')
                subj = next((l for l in lines if l.lower().startswith("subject:")), "Inquiry").replace("Subject:", "").strip()
                body = full_text.replace(subj, "").strip()[:100] + "..." # Sheet ke liye chota text

                # Update Sheet
                final_data = {
                    "Owner": ["Founding Partner"],
                    "Business": [biz],
                    "Niche": [niche],
                    "Mail": ["info@" + target_url.split('//')[-1].replace('www.', '')],
                    "Subject": [subj],
                    "Template": [full_text] # Poora template yahan save hoga
                }
                sheet_placeholder.dataframe(pd.DataFrame(final_data), use_container_width=True)
                st.success("✅ Done!")
                
                # Niche bara box for copy
                st.text_area("Full Mail Copy:", value=full_text, height=200)

            except Exception as e:
                st.error(f"Error: {str(e)}")
