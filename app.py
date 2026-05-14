import streamlit as st
import pandas as pd
import requests
import io
import random

# --- 1. BRANDING & STYLE ---
st.set_page_config(page_title="Rankiva Hub | Professional Outreach Engine", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1c1d; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e1e4e8; }
    .report-card { background-color: #f8f9fa; padding: 30px; border: 1px solid #e1e4e8; border-radius: 8px; }
    .copy-box { background-color: #ffffff; border: 1px solid #ff9000; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; }
    div.stButton > button:first-child {
        background-color: #ff9000 !important; color: white !important;
        height: 50px; width: 100%; font-weight: bold; border-radius: 4px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Outreach Settings")
    grq_key = st.text_input("Enter Groq API Key", type="password")
    st.divider()
    st.write("**Specialist:** Hafiz Amir Shahzad")
    st.caption("SEO Specialist | Rankiva Hub")

# --- 3. MAIN UI ---
st.markdown('<h1 style="color:#1a1c1d;">Rankiva Outreach Engine</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#525c65;">Analyze Ahrefs data and generate human-style personalized outreach emails.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    target_url = st.text_input("Website URL", value="https://redeepseek.com")
    biz_name = st.text_input("Business Name", value="Redeepseek")
with col2:
    owner_name = st.text_input("Owner Name", value="Not Found")
    biz_email = st.text_input("Business Email", value="Not Found")

st.markdown("### 📋 Paste Ahrefs Broken Link Data")
raw_data = st.text_area("Ahrefs table yahan paste karein", height=150)

# --- 4. ROTATION LOGIC & PROMPT ---
if st.button("Generate Personalized Outreach"):
    if not raw_data or not grq_key:
        st.error("Data aur API Key lazmi hai.")
    else:
        # Template selection (Rotating automatically)
        template_choice = random.choice([1, 2, 3])
        
        with st.spinner(f"Generating Outreach using Template {template_choice}..."):
            try:
                # Process data for the prompt
                data_io = io.StringIO(raw_data)
                df = pd.read_csv(data_io, sep='\t').head(5)
                broken_sample = df.to_string()

                # Professional AI Prompt with Strict Rules
                prompt = f"""
                You are a professional SEO specialist Hafiz Amir Shahzad from Rankiva Hub.
                Task: Write a personalized outreach email for {biz_name} ({target_url}).
                
                Data:
                Broken Links Found: {broken_sample}
                Owner: {owner_name}
                
                STRICT RULES:
                - Use Template {template_choice} style as a base but rewrite it to feel human.
                - No emojis. No Roman Urdu. No marketing buzzwords.
                - Tone: Calm, professional, and helpful.
                - Mention the broken link naturally.
                - Create urgency without being aggressive.
                - Follow the STRICT OUTPUT FORMAT provided in your instructions.
                """

                res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                     headers={"Authorization": f"Bearer {grq_key}"},
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
                
                st.session_state.final_output = res['choices'][0]['message']['content']
                st.session_state.audit_ready = True
            except Exception as e:
                st.error("Processing failed. Make sure data is copied correctly.")

# --- 5. OUTPUT DISPLAY ---
if 'audit_ready' in st.session_state:
    st.divider()
    st.markdown("### ✉️ Final Outreach Result")
    
    # Displaying the structured output
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.text(st.session_state.final_output)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.button("🔄 Generate Another (Rotate Template)")
    
