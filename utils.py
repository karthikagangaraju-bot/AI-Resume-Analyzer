import os
import openai
from docx import Document
from PyPDF2 import PdfReader

# Add stopwords to ignore non-skill words
STOPWORDS = set([
    "a", "an", "the", "and", "or", "in", "on", "for", "to", "of", "with",
    "is", "are", "be", "this", "needed", "required", "must", "should"
])

# Set your OpenAI API Key here
openai.api_key = "YOUR_API_KEY_HERE"


def extract_text(file):
    """
    Extract text from PDF, DOCX, or TXT files.
    """
    name = file.name.lower()
    text = ""
    if name.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    elif name.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + " "
    elif name.endswith(".txt"):
        text = file.read().decode("utf-8")
    else:
        text = ""
    return text.strip()


def analyze_resume(resume, job_desc):
    """
    Analyze resume and job description to calculate match score,
    matched skills, missing skills.
    """
    resume_words = set(
        word.lower().strip(",.") 
        for word in resume.split() 
        if word.lower() not in STOPWORDS
    )
    job_words = set(
        word.lower().strip(",.") 
        for word in job_desc.split() 
        if word.lower() not in STOPWORDS
    )

    matched_skills = resume_words.intersection(job_words)
    missing_skills = job_words - resume_words

    if len(job_words) == 0:
        score = 0
    else:
        score = int((len(matched_skills) / len(job_words)) * 100)

    return score, sorted(matched_skills), sorted(missing_skills)


def generate_resume_suggestion(missing_skills):
    """
    Provide suggestions to improve resume based on missing skills.
    """
    if not missing_skills:
        return "No suggestions needed! Your resume matches well 🎉"
    return "Consider adding these skills to improve your match:\n" + ", ".join(missing_skills)


def ask_ai(resume, job_desc, question):
    """
    Ask AI assistant for personalized resume advice.
    """
    prompt = f"""
    Resume: {resume}
    Job Description: {job_desc}
    Question: {question}
    Provide a concise professional answer with actionable suggestions.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"⚠️ AI response unavailable: {e}"
    return answer