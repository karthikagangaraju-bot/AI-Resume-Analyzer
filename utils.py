import PyPDF2

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def analyze_resume(resume, job_desc):
    resume_words = set(resume.lower().split())
    job_words = set(job_desc.lower().split())

    match = resume_words.intersection(job_words)
    score = int((len(match) / len(job_words)) * 100)

    missing = job_words - resume_words
    return score, list(missing)[:10]