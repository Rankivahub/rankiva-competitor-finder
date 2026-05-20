import streamlit as st
from playwright.sync_api import sync_playwright

def extract_data(target_url):
    with sync_playwright() as p:
        # Browser open karna (Chupky se)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url)
        
        # Yahan profile se data nikalne ka logic hai
        # Yeh example email/phone patterns dhoondne ke liye hai
        content = page.content()
        
        # Example Regex (Professional tool yahan heavy regex use karte hain)
        import re
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        phones = re.findall(r'\+\d{10,15}', content)
        
        browser.close()
        return list(set(emails)), list(set(phones))

# UI Interface
st.title("🎯 Rankiva OSINT Engine")
url = st.text_input("Target URL:")

if st.button("RUN DEEP EXTRACTION"):
    with st.spinner('Extremely hidden footprints searching...'):
        emails, phones = extract_data(url)
        
        st.success("Extraction Complete!")
        st.write("### Emails Found:", emails)
        st.write("### Numbers Found:", phones)
