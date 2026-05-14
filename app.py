import streamlit as st
import requests
import json

# --- RANKIVA GPT: SEARCH & CHAT EDITION ---
st.set_page_config(page_title="Rankiva GPT - Deep Search", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; min-width: 300px; }
    .stChatInput { border-radius: 10px; border: 1px solid #444c56 !important; background-color: #0d1117 !important; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 1. SERPER SEARCH ENGINE (Grok Style)
def fetch_live_data(query, serper_api_key):
    url = "https://google.serper.dev/search"
    headers = {'X-API-KEY': serper_api_key, 'Content-Type': 'application/json'}
    payload = json.dumps({"q": query})
    try:
        response = requests.post(url, headers=headers, data=payload)
        search_results = response.json()
        snippets = ""
        for item in search_results.get('organic', [])[:4]:
            snippets += f"\n- {item['title']}: {item['snippet']} (Source: {item['link']})"
        return snippets
    except:
        return "Search failed or API limit reached."

# 2. SESSION STATE (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. SIDEBAR (KEY MANAGEMENT)
with st.sidebar:
    st.title("Rankiva AI Dashboard")
    st.markdown("### 🔑 API Configurations")
    
    grq_key = st.text_input("Groq API Key", type="password", placeholder="Enter Groq Key...")
    serp_key = st.text_input("Serper API Key", type="password", placeholder="Enter Serper Key for Live Data...")
    
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.info("Agay Serper key enter ho jaye to ye internet se real-time data uthaye ga.")
    st.caption("Specialist: Hafiz Amir Shahzad")
    st.caption("Agency: Rankiva Hub")

# 4. CHAT DISPLAY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. CORE LOGIC
if prompt := st.chat_input("Ask me anything or paste SEO data..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not grq_key:
        st.error("Pehle sidebar mein Groq API Key enter karein.")
    else:
        with st.chat_message("assistant"):
            status_text = st.empty()
            try:
                web_data = ""
                # Search logic if Serper key is available
                if serp_key:
                    status_text.markdown("🔍 *Searching the web for latest info...*")
                    web_data = fetch_live_data(prompt, serp_key)
                
                status_text.markdown("🧠 *Analyzing and generating response...*")
                
                # Persona & Context
                system_instr = f"""
                You are Rankiva GPT, a high-level SEO Specialist named Hafiz Amir Shahzad.
                If provided, use this real-time web data to answer: {web_data}
                Always be professional, insightful, and helpful. If SEO data is provided, focus on audit and outreach.
                """
                
                history = [{"role": "system", "content": system_instr}] + st.session_state.messages[-6:]
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {grq_key}"},
                    json={"model": "llama-3.3-70b-versatile", "messages": history, "temperature": 0.6}
                ).json()

                final_answer = response['choices'][0]['message']['content']
                status_text.empty()
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

            except Exception as e:
                status_text.empty()
                st.error("Connection error. Please check your keys.")
                
