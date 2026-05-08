import streamlit as st
import requests
import google.generativeai as genai
from groq import Groq

# 1. PREMIUM THEME SETUP (Black, Gold, Emerald Green)
st.set_page_config(page_title="Rankiva Mega AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stButton>button { 
        background-color: #d4af37; color: black; font-weight: bold;
        border-radius: 8px; border: 2px solid #1e5631; width: 100%;
    }
    .stTextInput>div>div>input { background-color: #0b2d1a; color: #d4af37; border: 1px solid #d4af37; }
    h1 { color: #d4af37; text-align: center; border-bottom: 2px solid #1e5631; padding-bottom: 10px; }
    .stChatMessage { background-color: #0b2d1a; border-left: 5px solid #d4af37; border-radius: 10px; margin-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #051a0d; border-right: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 RANKIVA MEGA AI - SEO AGENT")

# 2. SIDEBAR CONFIG
st.sidebar.markdown("<h2 style='color: #d4af37;'>Control Center</h2>", unsafe_allow_html=True)
groq_key = st.sidebar.text_input("Groq API Key", type="password")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
serper_key = st.sidebar.text_input("Serper API Key", type="password")

# Initialize AI Clients
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

# 3. CHAT LOGIC
if prompt := st.chat_input("Mujh se kuch bhi puchen ya SEO leads dhoondo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not all([groq_key, gemini_key]):
            st.warning("Amir sahib, pehle sidebar mein Keys mukammal karen.")
        else:
            try:
                # Check for search intent
                search_words = ["dhoondo", "find", "search", "leads", "extract", "list"]
                is_search = any(word in prompt.lower() for word in search_words)

                if is_search and serper_key:
                    st.write("🔍 **Serper:** Data nikal raha hoon...")
                    url = "https://google.serper.dev/places"
                    res = requests.post(url, headers={'X-API-KEY': serper_key}, json={"q": prompt}).json().get('places', [])
                    
                    st.write("🧠 **Gemini:** Audit shuru hy...")
                    context = f"Analyze these leads for SEO specialist Amir Shahzad: {str(res[:5])}. Identify weak sites. Strategy in Urdu/English mix."
                    response = gemini_model.generate_content(context).text
                else:
                    # Updated Groq model to fix 400 error
                    chat_completion = groq_client.chat.completions.create(
                        messages=[{"role": "system", "content": "You are a friendly AI assistant for Amir Shahzad, founder of Rankiva Digital. Talk in Urdu/English mix."},
                                  {"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant"
                    )
                    response = chat_completion.choices[0].message.content

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
