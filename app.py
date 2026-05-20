import streamlit as st
from playwright.sync_api import sync_playwright
import re

# Page Configuration
st.set_page_config(page_title="Rankiva OSINT Engine", layout="wide")

def extract_data(target_url):
    try:
        with sync_playwright() as p:
            # Server-compatible browser launch
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page()
            page.goto(target_url, timeout=60000)
            
            content = page.content()
            
            # Extract Emails and WhatsApp numbers
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
            phones = re.findall(r'\+\d{10,15}', content)
            
            browser.close()
            return list(set(emails)), list(set(phones))
    except Exception as e:
        return None, str(e)

# UI Interface
st.title("🎯 Rankiva OSINT Engine")
url = st.text_input("Enter Target Profile URL (FB/IG/LI):")

if st.button("🚀 RUN DEEP EXTRACTION"):
    if url:
        with st.spinner('Accessing secure matrix...'):
            emails, error = extract_data(url)
            
            if emails is not None:
                st.success("Extraction Complete!")
                st.write("### 📧 Emails Found:", emails)
                st.write("### 📱 Numbers Found:", error) # Placeholder logic
            else:
                st.error(f"Error occurred: {error}")
    else:
        st.warning("Please provide a valid URL.")
