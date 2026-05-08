import streamlit as st
import requests
import google.generativeai as genai
from groq import Groq

# 1. LUXURY THEME SETUP
st.set_page_config(page_title="Rankiva Mega AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stButton>button { background-color: #d4af37; color: black; font-weight: bold; border-radius: 8px; width: 100%; }
    .stTextInput>div>div>input { background-color: #0b2d1a; color: #d4af37; border: 1px solid #d4af37; }
    h1 { color: #d4af37; text-align: center; border-bottom: 2px solid #1e5631; }
    .stChatMessage { background-color: #0b2d1a; border-left: 5px solid #d4af37; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #051a0d; border-right: 2px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 RANKIVA MEGA AI - Your Personal Assistant")

# 2. SIDEBAR CONFIG
st.sidebar.markdown("<h2 style='color: #d4af37;'>Control Center</h2>", unsafe_allow_html=True)
groq_key = st.sidebar.text_input("Groq API Key", type="password")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
serper_key = st.sidebar.text_input("Serper API Key", type="password")

# Initialize AI
if groq_key:
    groq_client = Groq(api_key=groq_key)
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. CONVERSATIONAL LOGIC
if prompt := st.chat_input("Mujh se kuch bhi puchen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not all([groq_key, gemini_key]):
            st.warning("Amir sahib, pehle Keys dalen.")
        else:
            try:
                # Check if it's a search request
                keywords = ["dhoondo", "find", "search", "leads", "extract"]
                is_search = any(word in prompt.lower() for word in keywords)

                if is_search and serper_key:
                    st.write("🔍 Searching live data...")
                    url = "https://google.serper.dev/places"
                    res = requests.post(url, headers={'X-API-KEY': serper_key}, json={"q": prompt}).json().get('places', [])
                    context = f"Analyze these leads for SEO specialist Amir Shahzad: {str(res[:5])}. Suggest outreach in Urdu/English."
                    response = gemini_model.generate_content(context).text
                else:
                    # General Chat using Groq for speed
                    chat_completion = groq_client.chat.completions.create(
                        messages=[{"role": "system", "content": "You are a helpful AI assistant for Amir Shahzad, founder of Rankiva Digital. Talk like a friendly colleague in Urdu/English mix."},
                                  {"role": "user", "content": prompt}],
                        model="llama3-8b-8192"
                    )
                    response = chat_completion.choices[0].message.content

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
