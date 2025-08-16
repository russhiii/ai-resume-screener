import streamlit as st
import os
from resume_parser import get_all_resumes, extract_keywords
from model import load_job_description, rank_resumes

st.set_page_config(page_title="AI Resume Screener", layout="wide")


st.sidebar.header("Job Description")
job_description = st.sidebar.text_area("Paste or write job description here:", height=200)

if job_description.strip() == "":
    st.sidebar.warning("Please enter the job description to rank resumes.")


st.title("📄 AI Resume Screener")
st.write("Upload resumes and match them against a job description using NLP.")

# Upload resumes
uploaded_files = st.file_uploader("📤 Upload new resume(s) (PDF only)", accept_multiple_files=True, type=['pdf'])
resume_folder = "resumes"

if not os.path.exists(resume_folder):
    os.makedirs(resume_folder)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = os.path.join(resume_folder, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")

# Load resumes
resumes_dict = get_all_resumes(resume_folder)

if job_description.strip() and resumes_dict:
    ranked_resumes = rank_resumes(job_description, resumes_dict)

    st.subheader("🏆 Ranked Resumes")
    for i, (filename, score) in enumerate(ranked_resumes, 1):
        st.markdown(f"**{i}. {filename}** — {'✅' if score > 0 else '❌'} Match Score: {score:.2f}")

else:
    st.info("Upload resumes and enter a job description to see ranked results.")
