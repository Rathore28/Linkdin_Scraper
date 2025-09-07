import streamlit as st
import pandas as pd
from linkedin_scraper import scrape_jobs
from visualize_jobs import visualize_jobs

st.set_page_config(page_title="LinkedIn Job Scraper", layout="wide")

st.title("💼 LinkedIn Job Scraper")

st.sidebar.header("Search Settings")
email = st.sidebar.text_input("LinkedIn Email")
password = st.sidebar.text_input("LinkedIn Password", type="password")
keyword = st.sidebar.text_input("Job Keyword", "Data Analyst")
location = st.sidebar.text_input("Location", "India")
num_jobs = st.sidebar.number_input("Number of Jobs", min_value=10, max_value=200, value=20, step=10)

if st.sidebar.button("Scrape Jobs"):
    if not email or not password:
        st.error("⚠️ Please enter your LinkedIn email and password.")
    else:
        with st.spinner("Scraping jobs from LinkedIn... Please wait ⏳"):
            df = scrape_jobs(email, password, keyword, location, num_jobs)
            if not df.empty:
                st.success(f"✅ Found {len(df)} jobs!")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", csv, "jobs.csv", "text/csv")

                # Visualization
                img_file = visualize_jobs(df)
                st.image(img_file, caption="Top Hiring Companies", use_column_width=True)
            else:
                st.warning("No jobs found. Try changing your search.")
