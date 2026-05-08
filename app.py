import streamlit as st
import requests
import google.generativeai as genai
from groq import Groq

# 1. LUXURY THEME SETUP (Black, Gold, Emerald Green)
st.set_page_config(page_title="Rankiva Mega AI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stButton>button { 
        background-color: #d4af37; color: black; font-weight: bold;
        border-radius: 10px; border: 2px solid #1e5631;
    }
    .stTextInput>div>div>input { background-color: #0b2d1a; color: #d4af37; border: 1px solid #d4af37; }
    h1 { color: #d4af37; text-align: center; border-bottom: 2px solid #1e5631; padding-bottom: 10px; }
    .stChatMessage { background-color: #0b2d1a; border-left: 5px solid #d4af37; }
    .sidebar .sidebar-content { background-color: #000000; }
    </style>
    """, unsafe_allow_input_True)

st.title("🏆 RANKIVA MEGA AI - Premium SEO Agent")

# 2. SIDEBAR CONFIGURATION
st.sidebar.markdown("<h2 style='color: #d4af37;'>Settings</h2>", unsafe_allow_input_True)
groq_key = st.sidebar.text_input("Groq API Key (Fast Chat)", type="password")
gemini_key = st.sidebar.text_input("Gemini API Key (Audit)", type="password")
serper_key = st.sidebar.text_input("Serper API Key (Search)", type="password")

# Initialize AI Clients
if groq_key:
    groq_client = Groq(api_key=groq_key)
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# 3. CHAT INTERFACE
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Amir: Dhoondo weak roofing sites in Auckland..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not all([groq_key, gemini_key, serper_key]):
            st.error("Pehle teeno (3) Keys sidebar mein dalen!")
        else:
            # Step A: Serper Search
            st.write("🟢 **Serper:** Data nikal raha hoon...")
            url = "https://google.serper.dev/places"
            payload = {"q": prompt}
            headers = {'X-API-KEY': serper_key, 'Content-Type': 'application/json'}
            res = requests.post(url, headers=headers, json=payload).json().get('places', [])
            
            # Step B: Gemini Audit (High Quality Analysis)
            st.write("🟡 **Gemini:** SEO Audit ho raha hy...")
            audit_query = f"Audit these leads for SEO gaps: {str(res[:5])}. Give priority to 'No Website' or 'Low Reviews'. Answer in Urdu/English mix."
            audit_report = gemini_model.generate_content(audit_query).text
            
            # Step C: Groq Response (Lightning Fast Delivery)
            st.write("⚡ **Groq:** Report finalize ho rahi hy...")
            final_chat = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": f"Summarize this SEO report for Amir Shahzad: {audit_report}"}],
                model="llama3-8b-8192"
            ).choices[0].message.content
            
            st.markdown(final_chat)
            st.session_state.messages.append({"role": "assistant", "content": final_chat})
