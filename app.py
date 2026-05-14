import streamlit as st
import requests

# --- FORCED UPDATE VERSION 3.0 ---
st.set_page_config(page_title="Rankiva GPT", layout="centered")

# CSS for a clean ChatGPT look
st.markdown("""
    <style>
    .stApp { background-color: #212121; color: #ececec; }
    section[data-testid="stSidebar"] { background-color: #171717; }
    .stChatInput { border-radius: 25px; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Key
with st.sidebar:
    st.title("Rankiva Hub")
    st.write("Specialist: Hafiz Amir Shahzad")
    st.divider()
    grq_key = st.text_input("Groq API Key", type="password")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Message Rankiva GPT..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API Call
    if not grq_key:
        st.error("Pehle sidebar mein Groq API Key dalein.")
    else:
        with st.chat_message("assistant"):
            try:
                # Persona logic
                persona = "You are Rankiva GPT, a professional SEO specialist Hafiz Amir Shahzad. Answer in a deep, helpful, and human tone."
                history = [{"role": "system", "content": persona}] + st.session_state.messages
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {grq_key}"},
                    json={"model": "llama-3.3-70b-versatile", "messages": history}
                ).json()

                full_res = response['choices'][0]['message']['content']
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except:
                st.error("System Error: Key ya Internet check karein.")
                
