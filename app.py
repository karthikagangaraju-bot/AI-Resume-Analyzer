import streamlit as st
from utils import extract_text, analyze_resume

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_desc = st.text_area("Paste Job Description")

if uploaded_file and job_desc:
    resume_text = extract_text(uploaded_file)
    score, missing_skills = analyze_resume(resume_text, job_desc)

    st.subheader(f"Match Score: {score}%")
    st.write("Missing Skills:", missing_skills)