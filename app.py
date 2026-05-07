import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Rankiva Digital - SEO Lead Machine", layout="wide")
st.title("🎯 RANKIVA DIGITAL - Outreach Tool")

api_key = st.sidebar.text_input("Serper API Key", type="password")

# Inputs
col1, col2, col3 = st.columns(3)
with col1:
    business_type = st.text_input("Business Name / Niche", "Plumbing")
with col2:
    city_name = st.text_input("City", "Tauranga")
with col3:
    country = st.selectbox("Country", ["New Zealand", "Australia", "USA", "UK", "Pakistan"])

if st.button("GET LEADS & WRITE EMAILS"):
    if not api_key:
        st.error("Sidebar mein API Key dalen!")
    else:
        url = "https://google.serper.dev/places"
        payload = {"q": f"{business_type} in {city_name} {country}"}
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}

        with st.spinner('Scanning Google Maps and drafting your personal emails...'):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                results = response.json().get('places', [])
                outreach_data = []

                for item in results:
                    b_name = item.get('title', 'Business Owner')
                    web_url = item.get('website', 'No Website')
                    
                    # --- Updated Template with your Name ---
                    subject = f"Feedback on your website - {b_name}"
                    email_body = (
                        f"Hi {b_name} Team,\n\n"
                        f"I was recently browsing through local services in {city_name} and spent some time on your website. "
                        f"I have to say, your {business_type} page is one of the best I’ve seen in terms of clarity and building trust with homeowners.\n\n"
                        f"I’m Hafiz Amir Shahzad, an SEO specialist and founder of Rankiva Digital. Usually, I see websites that are cluttered, but yours has great potential. "
                        f"With a little more 'Topical Authority' (adding some specific blog guides), I believe you could easily dominate the first page of Google in your area.\n\n"
                        f"Have you ever considered adding an FAQ or a local blog section to boost your reach?\n\n"
                        f"Best regards,\n"
                        f"Hafiz Amir Shahzad\n"
                        f"SEO Specialist | Rankiva Digital"
                    )

                    outreach_data.append({
                        "Business Name": b_name,
                        "Website": web_url,
                        "Email Subject": subject,
                        "Full Email": email_body
                    })

                if outreach_data:
                    df = pd.DataFrame(outreach_data)
                    st.success(f"Mubarak ho! {len(df)} leads aur Hafiz Amir Shahzad ke naam ki emails tayyar hain.")
                    
                    # Display Table
                    st.dataframe(df)

                    # Download CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download outreach_list.csv", csv, "rankiva_outreach.csv", "text/csv")
                else:
                    st.warning("Koi results nahi mile.")
            else:
                st.error("API Error! Key check karen.")
