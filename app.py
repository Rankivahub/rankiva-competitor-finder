import streamlit as st
import pandas as pd
import requests
import random

# --- 1. SETTINGS & STYLING (THE LOOK YOU WANT) ---
st.set_page_config(page_title="Rankiva AI Specialist", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    /* Sidebar Chat Style */
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; min-width: 280px; }
    .chat-history-item { padding: 10px; border-radius: 8px; margin-bottom: 5px; background: #21262d; color: #c9d1d9; font-size: 14px; border: 1px solid #30363d; }
    
    /* Result Columns */
    .output-column { background: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 12px; min-height: 250px; }
    .label-style { color: #8b949e; font-size: 13px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff9000, #ff5e00) !important; color: white !important;
        border: none !important; border-radius: 8px !important; font-weight: bold !important; width: 100% !important; height: 45px !important;
    }
    input, textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (HISTORY & KEY) ---
with st.sidebar:
    st.markdown("### 💬 Chat History")
    st.markdown('<div class="chat-history-item">🔍 Audit: redeepseek.com</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-history-item">📧 Outreach: Real Estate UK</div>', unsafe_allow_html=True)
    st.divider()
    grq_key = st.text_input("Enter Groq API Key", type="password")
    st.divider()
    st.caption("Specialist: Hafiz Amir Shahzad")
    st.caption("Agency: Rankiva Hub")

# --- 3. MAIN INTERFACE ---
st.markdown("<h2 style='margin-bottom:0;'>Rankiva Intelligent Auditor</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;'>Deep Search & Specialized Outreach System</p>", unsafe_allow_html=True)

# Input Section
target_url = st.text_input("Target URL", placeholder="https://example.com")
raw_data = st.text_area("Paste Ahrefs Data / Ask something...", height=150)

if st.button("Run Deep Analysis"):
    if not grq_key or not raw_data:
        st.error("Please provide your Groq Key and Data first.")
    else:
        template_id = random.choice([1, 2, 3])
        with st.spinner("Processing like Grok..."):
            try:
                prompt = f"""
                Act as a professional SEO Specialist Hafiz Amir Shahzad.
                Analyze this data for {target_url}: {raw_data[:1500]}
                Use Template {template_id} style but keep it human.
                
                Format the output exactly:
                SUBJECT: [Subject]
                ---
                BODY: [Email Body]
                """
                
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                     headers={"Authorization": f"Bearer {grq_key}"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
                
                full_content = res['choices'][0]['message']['content']
                
                if "---" in full_content:
                    st.session_state.sub_final = full_content.split("---")[0].replace("SUBJECT:", "").strip()
                    st.session_state.body_final = full_content.split("---")[1].replace("BODY:", "").strip()
                else:
                    st.session_state.sub_final = f"Quick note regarding {target_url}"
                    st.session_state.body_final = full_content
                
                st.session_state.ready = True
            except:
                st.error("API Connection Error.")

# --- 4. DUAL COLUMN OUTPUT ---
if 'ready' in st.session_state:
    st.divider()
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="label-style">Generated Subject</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-column">{st.session_state.sub_final}</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="label-style">Professional Email Content</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-column">{st.session_state.body_final}</div>', unsafe_allow_html=True)

# --- 5. CHAT INPUT (BOTTOM) ---
st.divider()
st.chat_input("Follow-up: 'Make it more urgent' or 'Translate to English'...")
