import streamlit as st
import requests
import pandas as pd
import re

st.set_page_config(page_title="Rankiva Digital - SEO Prospector", layout="wide")
st.title("🔍 RANKIVA DIGITAL - SEO Lead Prospector (Hot/Cold)")

api_key = st.sidebar.text_input("Serper API Key", type="password")

# Input Section
col1, col2, col3 = st.columns(3)
with col1:
    niche = st.text_input("Business Niche", "Roofing")
with col2:
    city = st.text_input("City Name", "Tauranga")
with col3:
    country = st.selectbox("Select Country", ["New Zealand", "Australia", "USA", "UK", "Canada"])

def get_seo_status(reviews, rating):
    if reviews <= 15 or rating < 4.0:
        return "🔥 HOT (Low SEO/Traffic)"
    elif reviews > 15 and reviews <= 50:
        return "⚖️ WARM (Needs Improvement)"
    else:
        return "❄️ COLD (Strong SEO)"

if st.button("EXTRACT SEO LEADS"):
    if not api_key:
        st.error("Pehle API Key dalen!")
    else:
        url = "https://google.serper.dev/places"
        payload = {"q": f"{niche} in {city} {country}"}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        with st.spinner('Scraping Map Data & Analyzing SEO...'):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                results = response.json().get('places', [])
                lead_list = []

                for item in results:
                    reviews = item.get('ratingCount', 0)
                    rating = item.get('rating', 0)
                    website = item.get('website', 'No Website')
                    
                    # Determining SEO Status
                    status = get_seo_status(reviews, rating)
                    
                    # Logic for Email (Based on common patterns)
                    # Note: Direct email scraping needs a separate tool, 
                    # but we can provide the domain for your manual outreach
                    lead_list.append({
                        "Status": status,
                        "Business Name": item.get('title'),
                        "Reviews": reviews,
                        "Rating": rating,
                        "Website": website,
                        "Phone": item.get('phoneNumber', 'N/A'),
                        "Address": item.get('address'),
                        "Potential Email": f"info@{website.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]}" if website != "No Website" else "N/A"
                    })

                if lead_list:
                    df = pd.DataFrame(lead_list)
                    # Sort by Status to show HOT leads first
                    df = df.sort_values(by="Status", ascending=False)
                    
                    st.success(f"Hamain {len(df)} leads mili hain. 'HOT' wali leads par tawajjo den!")
                    st.dataframe(df)

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Rankiva_Lead_Sheet.csv", csv, "rankiva_leads.csv", "text/csv")
                else:
                    st.warning("Koi results nahi mile.")
            else:
                st.error("API Error!")
