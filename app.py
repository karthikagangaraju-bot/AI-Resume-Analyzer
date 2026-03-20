import streamlit as st
from utils import extract_text, analyze_resume, generate_resume_suggestion, ask_ai

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("AI Resume Analyzer 🚀")
st.markdown("Upload your resume (PDF, DOCX, TXT) and paste the job description to get a detailed analysis.")

# Upload Resume
uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "docx", "txt"])
if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("Resume uploaded successfully!")

# Paste Job Description
job_desc = st.text_area("Paste Job Description")

# Analyze Button
if st.button("Analyze Resume") and uploaded_file and job_desc.strip() != "":
    score, matched_skills, missing_skills = analyze_resume(resume_text, job_desc)

    # Match Score Section
    st.subheader("Match Score")
    st.progress(score / 100)
    if score > 70:
        st.success(f"{score}% 🎯 Excellent match!")
    elif score > 40:
        st.warning(f"{score}% ⚠️ Moderate match. Some improvements can boost your score.")
    else:
        st.error(f"{score}% 🚧 Low match. Significant improvements are needed.")

    # Matched Skills
    st.subheader("Matched Skills")
    if matched_skills:
        st.write(", ".join(matched_skills))
    else:
        st.write("No matched skills found.")

    # Missing Skills
    st.subheader("Missing Skills")
    if missing_skills:
        st.write(", ".join(missing_skills))
    else:
        st.write("No missing skills! Your resume matches well 🎉")

    # Suggestions
    st.subheader("Suggestions to Improve")
    st.write(generate_resume_suggestion(missing_skills))

    # Generated Resume Suggestion
    with st.expander("Generated Resume Suggestion"):
        st.text(generate_resume_suggestion(missing_skills))

# AI Assistant
st.subheader("Ask AI about your Resume or Job Fit")
user_question = st.text_input("Type your question here...")
if st.button("Ask AI") and uploaded_file and job_desc.strip() != "" and user_question.strip() != "":
    ai_response = ask_ai(resume_text, job_desc, user_question)
    st.text_area("AI Answer", value=ai_response, height=150)