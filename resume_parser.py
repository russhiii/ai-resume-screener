import os
from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Uncomment these lines and run once in a Python shell to download NLTK data:
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

def get_all_resumes(resume_folder="resumes"):
    resumes = {}
    # Create folder if it doesn't exist
    if not os.path.exists(resume_folder):
        os.makedirs(resume_folder)

    for filename in os.listdir(resume_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(resume_folder, filename)
            with open(path, "rb") as f:
                reader = PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                resumes[filename] = text
    return resumes

def extract_keywords(text, num_keywords=10):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    # Filter words: only alphabets and not stopwords
    words = [w for w in words if w.isalpha() and w not in stop_words]

    freq_dist = nltk.FreqDist(words)
    keywords = [word for word, freq in freq_dist.most_common(num_keywords)]
    return keywords
