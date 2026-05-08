import streamlit as st
import requests
import google.generativeai as genai
from groq import Groq

# 1. PREMIUM THEME SETUP (Black, Gold, Emerald Green)
st.set_page_config(page_title="Rankiva Mega AI", layout="wide")

# CSS for a High-End SEO Dashboard Look
st.markdown("""
    <style>
    /* Main Background */
    .stApp { 
        background-color: #000000; 
        color: #ffffff; 
    }
    /* Button Styling */
    .stButton>button { 
        background-color: #d4af37; 
        color: black; 
        font-weight: bold;
        border-radius: 8px; 
        border: 2px solid #1e5631; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e5631;
        color: #d4af37;
        border: 2px solid #d4af37;
    }
    /* Input Fields */
    .stTextInput>div>div>input { 
        background-color: #0b2d1a; 
        color: #d4af37; 
        border: 1px solid #d4af37; 
    }
    /* Headings */
    h1 { 
        color: #d4af37; 
        text-align: center; 
        border-bottom: 2px solid #1e5631; 
        padding-bottom: 10px;
        font-family: 'Times New Roman', serif;
    }
    /* Chat Bubbles */
    .stChatMessage { 
        background-color: #0b2d1a; 
        border-left: 5px solid #d4af37; 
        border-radius: 10px; 
        margin-bottom: 15px;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] { 
        background-color: #051a0d; 
        border-right: 2px solid #d4af37; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 RANKIVA MEGA AI - SEO LEAD AGENT")

# 2. SIDEBAR - API KEYS
st.sidebar.markdown("<h2 style='color: #d4af37;'>Rankiva Control Center</h2>", unsafe_allow_html=True)
st.sidebar.info("Teeno Keys dalen taakay AI activate ho sakay.")

groq_key = st.sidebar.text_input("1. Groq API Key (Speed)", type="password")
gemini_key = st.sidebar.text_input("2. Gemini API Key (Deep Audit)", type="password")
serper_key = st.sidebar.text_input("3. Serper API Key (Live Data)", type="password")

# Initialize Clients
if groq_key:
    groq_client = Groq(api_key=groq_key)
if gemini_key:
    genai.configure(api_key=gemini_key)
    # Updated model name to fix 404 error
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 3. CHAT HISTORY MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. MAIN ACTION
if prompt := st.chat_input("E.g., Find weak SEO real estate sites in Italy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not all([groq_key, gemini_key, serper_key]):
            st.warning("Amir sahib, pehle sidebar mein teeno (3) Keys mukammal karen.")
        else:
            try:
                # Step A: Fetch Live Leads via Serper
                st.write("🟢 **Scanning Google Maps...**")
                search_url = "https://google.serper.dev/places"
                payload = {"q": prompt}
                headers = {'X-API-KEY': serper_key, 'Content-Type': 'application/json'}
                response = requests.post(search_url, headers=headers, json=payload).json()
                results = response.get('places', [])

                if not results:
                    st.error("Koi leads nahi mili, query thori tabdeel karen.")
                else:
                    # Step B: Strategic Audit via Gemini
                    st.write("🟡 **Gemini 1.5 is analyzing SEO Gaps...**")
                    audit_context = (
                        f"User is Amir Shahzad, founder of Rankiva Digital. "
                        f"Analyze these 5 leads for SEO opportunities: {str(results[:5])}. "
                        f"Identify missing websites or low reviews. Give a winning outreach strategy in Urdu/English mix."
                    )
                    audit_output = gemini_model.generate_content(audit_context).text

                    # Step C: Final Polish & Speed via Groq
                    st.write("⚡ **Groq is finalizing the report...**")
                    final_summary = groq_client.chat.completions.create(
                        messages=[{"role": "system", "content": "You are a professional SEO assistant. Format the report cleanly with bullet points."},
                                  {"role": "user", "content": audit_output}],
                        model="llama3-8b-8192"
                    ).choices[0].message.content

                    # Show Results
                    st.markdown(final_summary)
                    st.session_state.messages.append({"role": "assistant", "content": final_summary})
                    
            except Exception as e:
                st.error(f"System Error: {str(e)}")
