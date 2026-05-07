import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Rankiva Digital - Lead Generator", layout="wide")
st.title("🚀 RANKIVA DIGITAL - Map & SEO Lead Finder")

# Sidebar for API Key
api_key = st.sidebar.text_input("Serper API Key", type="password")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    query = st.text_input("Kya dhoondna hy? (e.g. Plumbers in Tauranga)", "Real Estate in Auckland")
with col2:
    min_reviews = st.number_input("Maximum Reviews (SEO Weakness)", value=10, help="Jin businesses ke reviews is se kam honge, wahi nazar aayenge.")

if st.button("GENERATE WEAK SEO LEADS"):
    if not api_key:
        st.error("Pehle Sidebar mein API Key dalen!")
    else:
        # Maps (Places) API use kar rahe hain taakay Maps ka data aaye
        url = "https://google.serper.dev/places"
        payload = {"q": query}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        with st.spinner('Maps aur SEO Data fetch ho raha hai...'):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                results = response.json().get('places', [])
                
                # Filter: Sirf wo jin ki SEO/Reviews weak hain
                weak_leads = []
                for item in results:
                    reviews = item.get('ratingCount', 0)
                    rating = item.get('rating', 0)
                    
                    if reviews <= min_reviews: # Filter logic
                        weak_leads.append({
                            "Business Name": item.get('title'),
                            "Address": item.get('address'),
                            "Rating": rating,
                            "Reviews": reviews,
                            "Website": item.get('website', 'No Website'),
                            "Phone": item.get('phoneNumber', 'N/A'),
                            "Status": "Weak SEO / Low Reviews"
                        })
                
                if weak_leads:
                    df = pd.DataFrame(weak_leads)
                    st.success(f"Hamain {len(df)} aisi companies mili hain jin ki SEO behtar ki ja sakti hai!")
                    st.table(df)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Weak Leads (Excel)", csv, "rankiva_leads.csv", "text/csv")
                else:
                    st.warning("Koi aisi site nahi mili jis ke reviews itne kam hon. Filter thora barha kar check karen.")
            else:
                st.error("API Response mein masla hy. Key check karen.")
