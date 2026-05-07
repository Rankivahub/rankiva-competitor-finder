import streamlit as st
import requests
import pandas as pd

# Page Configuration (Interface Setup)
st.set_page_config(page_title="Rankiva Digital - Competitor Finder", layout="wide")

st.title("🚀 RANKIVA DIGITAL - Competitor Finder")
st.write("Niche, City, aur Country likhen taakay aap apne competitors dhoond saken.")

# User Inputs (Design Boxes)
col1, col2, col3 = st.columns(3)
with col1:
    niche = st.text_input("Niche / Business Type", "Real Estate")
with col2:
    city = st.text_input("City", "Tauranga")
with col3:
    country = st.text_input("Country", "New Zealand")

api_key = st.sidebar.text_input("Serper API Key", type="password")

if st.button("FIND COMPETITORS"):
    if not api_key:
        st.error("Pehle sidebar mein apni Serper API Key dalen!")
    else:
        query = f"{niche} in {city} {country}"
        url = "https://google.serper.dev/search"
        payload = {"q": query, "num": 100}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        with st.spinner('Data fetch ho raha hai...'):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                results = response.json().get('organic', [])
                data = []
                for item in results:
                    data.append({
                        "Business Name": item.get('title'),
                        "Website": item.get('link'),
                        "Description": item.get('snippet'),
                        "Rank": results.index(item) + 1
                    })
                
                df = pd.DataFrame(data)
                
                # Show Result Table (Bilkul image ki tarah)
                st.success(f"{len(df)} Competitors mil gaye hain!")
                st.table(df)
                
                # Download Button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV (Excel)", csv, "rankiva_leads.csv", "text/csv")
            else:
                st.error("API Key kaam nahi kar rahi.")
