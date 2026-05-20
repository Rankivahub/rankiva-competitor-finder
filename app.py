import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("🎯 Rankiva OSINT Engine (Stable)")
url = st.text_input("Enter Target Website URL:")

if st.button("🚀 RUN EXTRACTION"):
    if url:
        try:
            with st.spinner('Scanning site...'):
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                
                # Regex for Email and WhatsApp
                emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))
                phones = list(set(re.findall(r'\+?\d{10,15}', text)))
                
                st.success("Extraction Complete!")
                st.write("### 📧 Emails Found:", emails)
                st.write("### 📱 Numbers Found:", phones)
        except Exception as e:
            st.error(f"Error: {e}")
