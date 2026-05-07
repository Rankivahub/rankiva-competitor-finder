import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Rankiva Lead & Mailer", layout="wide")
st.title("🎯 RANKIVA DIGITAL - Lead Finder & Auto Mailer")

api_key = st.sidebar.text_input("Serper API Key", type="password")

col1, col2, col3 = st.columns(3)
with col1:
    business = st.text_input("Business Name", "Plumber")
with col2:
    city = st.text_input("City", "Tauranga")
with col3:
    country = st.selectbox("Country", ["New Zealand", "Australia", "USA", "UK"])

if st.button("GENERATE LEADS & EMAILS"):
    if not api_key:
        st.error("Sidebar mein API Key dalen!")
    else:
        url = "https://google.serper.dev/places"
        payload = {"q": f"{business} in {city} {country}"}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        with st.spinner('Scrutinizing leads and writing emails...'):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                results = response.json().get('places', [])
                final_data = []
                
                for item in results:
                    name = item.get('title')
                    rev = item.get('ratingCount', 0)
                    rat = item.get('rating', 0)
                    web = item.get('website')
                    
                    # --- AI Email Logic (Trust Building) ---
                    if not web:
                        subject = f"Question about {name}'s online presence"
                        body = f"Hi {name} Team,\n\nI was looking for {business} services in {city} and couldn't find your website. In 2026, 90% of customers book online. I can help you get a professional site to capture these leads.\n\nBest,\nRankiva Digital"
                    elif rev < 10:
                        subject = f"Improving {name}'s Google visibility"
                        body = f"Hi {name} Team,\n\nI noticed your business has great potential but only {rev} reviews. This is making your competitors rank higher. I have a strategy to boost your rating and organic traffic.\n\nRegards,\nRankiva Digital"
                    else:
                        subject = f"Growth strategy for {name}"
                        body = f"Hi {name},\n\nYour {rat} star rating is good, but you're missing out on top-page traffic for '{business}' in {city}. Can we discuss an SEO audit?\n\nBest,\nRankiva Digital"

                    final_data.append({
                        "Business Name": name,
                        "Website": web if web else "NO WEBSITE",
                        "Reviews": rev,
                        "Email Subject": subject,
                        "Email Content": body
                    })
                
                df = pd.DataFrame(final_data)
                st.success("Data aur Personalized Emails tayyar hain!")
                st.dataframe(df)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data + Emails", csv, "rankiva_outreach.csv", "text/csv")
