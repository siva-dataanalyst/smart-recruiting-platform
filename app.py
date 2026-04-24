import streamlit as st
import PyPDF2 
import io
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page config
st.set_page_config(
    page_title = "Smart Recruiting Platform",
    page_icon = "🎯",
    layout = "wide"
)


# Title
st.title("🎯 Smart Recruiting Platform")
st.subheader("Phase 1 - Resume Upload & Text Extraction")
st.markdown("---")


# File uploader
uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF only)",
    type="pdf"
)


# Function to extract text
def extract_text_from_pdf(file):
    pdf_reader=PyPDF2.PdfReader(file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()
    return text


# Show results after upload
if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")

    extracted_text=extract_text_from_pdf(uploaded_file)

    st.subheader("📋 Extracted Resume Content")
    st.text_area("Resume Text",extracted_text,height=400)

    st.info(f"📊 Total characters extracted: {len(extracted_text)}")
else:
    st.warning("⬆️ Please upload a resume PDF to get started")



# Phase 2- Job Description Input & Skill Matching
st.markdown("---")
st.subheader("📝 Phase 2 - Job Description & Skill Matching")


# Job Description Input
job_description=st.text_area(
    "Paste Job Description Here",
    height=200,
    placeholder="Paste the job description here..."
)


# Let recruiter enter required skills
skills_input=st.text_input(
    "Enter required skills (comma separated)",
    placeholder="python, sql, power bi, excel..."
)

# Funtion to match skills
def match_skills(resume_text,skills_list):
    resume_text=resume_text.lower()
    matched=[]
    unmatched=[]
    for skill in skills_list:
        if skill in resume_text:
            matched.append(skill)
        else:
            unmatched.append(skill)
    return matched , unmatched
# Show results
if uploaded_file is not None and skills_input:
    # Convert input to list
    skills_list=[skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    matched_skills , unmatched_skills = match_skills(
        extracted_text,skills_list
    )
    st.markdown("---")
    st.subheader("📊 Skill Match Results")

    # Match score
    score=len(matched_skills)/len(skills_list) * 100

    # Display score
    st.info(f"📊 Match Score: {score:.1f}%")

    # Display Matched skills
    st.success(f"✅ Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}")

    # Display unmatched skills
    st.error(f"❌ Missing Skills: {', '.join(unmatched_skills) if unmatched_skills else 'None'}")


# Phase 3 - ML Scoring & Candidate Ranking
st.markdown("---")
st.subheader("🏆 Phase 3 - ML Scoring & Candidate Ranking")

# Multiple Resume Uploader
uploaded_resumes=st.file_uploader(
    "📄 Upload Multiple Resumes (PDF only)",
    type="pdf",
    accept_multiple_files=True
)

# ML Scoring Function
def calculate_ml_score(resume_text,job_desc):
    vectorizer=TfidfVectorizer()
    vectors=vectorizer.fit_transform([resume_text,job_desc])
    score=cosine_similarity(vectors[0],vectors[1])[0][0]
    return round(score*100,2)

# Show Ranking Results
if uploaded_resumes and job_description:
    st.markdown("---")
    st.subheader("📊 Candidate Ranking Results")

    candidates=[]

    for resume in uploaded_resumes:
        text=extract_text_from_pdf(resume)
        score=calculate_ml_score(text,job_description)
        candidates.append({
            "Candidate": resume.name,
            "ML Score": score
        })

    # Create Dataframe sort by score
    df=pd.DataFrame(candidates)
    df=df.sort_values("ML Score",ascending=False)
    df["Rank"]=range(1,len(df)+1)
    df=df[["Rank","Candidate","ML Score"]]

    st.dataframe(df,use_container_width=True)

    # Show top candidates 
    top=df.iloc[0]
    st.success(f"🏆 Top Candidate: {top['Candidate']} with ML Score: {top['ML Score']}%")