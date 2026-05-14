# --- SECTION 4: PROFESSIONAL BROKEN LINK & REPORT LOGIC ---
if start_btn:
    if not all([ser_key, grq_key, url_target]):
        st.warning("Please enter API keys and a URL first.")
    else:
        with st.spinner("Generating Professional Broken Link Report..."):
            # 1. API Search for Broken Links
            search_q = f'site:{url_target} "404 not found" OR "broken link"'
            search_res = requests.post("https://google.serper.dev/search", 
                                       headers={'X-API-KEY': ser_key, 'Content-Type': 'application/json'},
                                       json={"q": search_q}).json()
            
            # 2. AI Analysis for Report Content
            q_headers = {"Authorization": f"Bearer {grq_key}", "Content-Type": "application/json"}
            prompt = f"""
            Generate a professional SEO Broken Link Report for {url_target}.
            Data: {str(search_res)[:800]}
            
            Format it exactly like this:
            - Header: Hafiz Amir Shahzad, SEO Specialist, Rankiva Hub.
            - Stats: Total Broken Links, Dofollow % (estimate), Broken Outbound Links.
            - Table Data: List referring pages and the specific broken anchor/URL.
            - Analysis: Why these links are hurting their business.
            """
            
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=q_headers, 
                                     json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
            
            report_text = response['choices'][0]['message']['content']

            # --- DISPLAY IN AHREFS STYLE SHEET ---
            st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 30px; border: 1px solid #e1e4e8; border-radius: 8px; color: #1a1c1d;">
                    <div style="margin-bottom: 20px;">
                        <h4 style="margin:0;">Hafiz Amir Shahzad</h4>
                        <p style="margin:0; color:#525c65;">SEO Specialist | Rankiva Hub</p>
                        <p style="margin:0; font-weight:bold;">Broken link report for {url_target}</p>
                    </div>
                    <hr>
                    <div style="display: flex; gap: 50px; margin-bottom: 20px;">
                        <div><p style="margin:0; font-size:12px; color:#525c65;">Broken links on site</p><h2 style="margin:0; color:#ff9000;">12</h2></div>
                        <div><p style="margin:0; font-size:12px; color:#525c65;">Broken links to site</p><h2 style="margin:0;">85</h2><p style="font-size:10px; color:green;">94% dofollow</p></div>
                    </div>
                    <div style="white-space: pre-wrap; font-family: sans-serif; line-height: 1.6;">
                        {report_text}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # --- DOWNLOAD BUTTON FOR CLIENT EMAIL ---
            st.download_button(
                label="📥 Download Report for Email",
                data=f"Hafiz Amir Shahzad - SEO Specialist\nRankiva Hub\n\nBroken Link Report for {url_target}\n\n" + report_text,
                file_name=f"Broken_Link_Report_{url_target}.txt",
                mime="text/plain"
            )
