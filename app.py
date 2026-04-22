import streamlit as st
import PyPDF2 
import io

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