import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

def load_job_description(path='job_description.txt'):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def rank_resumes(resumes_dict, job_description):
    jd_clean = clean_text(job_description)
    resume_names = list(resumes_dict.keys())
    resume_texts = [clean_text(resumes_dict[name]) for name in resume_names]

    documents = [jd_clean] + resume_texts
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    jd_vector = vectors[0]
    resume_vectors = vectors[1:]

    scores = cosine_similarity(jd_vector, resume_vectors)[0]

    ranked = sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True)
    return ranked
