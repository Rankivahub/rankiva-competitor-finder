import streamlit as st

def render_analysis_modal():
    st.markdown('<div style="background-color: #112240; padding: 20px; border-radius: 15px;">', unsafe_allow_html=True)
    st.subheader("SEO Site Audit")
    domain = st.text_input("Enter domain (e.g., example.com)")
    if st.button("Analyze Now"):
        st.write(f"Analyzing {domain}...")
    st.markdown('</div>', unsafe_allow_html=True)
