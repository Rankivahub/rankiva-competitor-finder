import streamlit as st

# Yeh tarika hai HTML aur Python ko milane ka
st.markdown("""
    <div style="background:#fff; padding:25px; border-radius:8px; border:1px solid #e2e8f0;">
        <h2 style="color:#aa7c11;">Advanced Target Extractor</h2>
    </div>
""", unsafe_allow_html=True)

# Input aur Button
url = st.text_input("Enter URL:")
if st.button("Start Extraction"):
    st.write("Processing... " + url)
