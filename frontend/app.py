import os
from pathlib import Path
import streamlit as st
import base64
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")

if not N8N_WEBHOOK:
    st.error("❌ N8N_WEBHOOK_URL missing in .env")

# -------------------------------------------------------
# BEAUTIFUL UI CSS
# -------------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}
.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #1a73e8;
    text-align: center;
    margin-bottom: -5px;
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #fff;
    margin-bottom: 25px;
}
.stButton>button {
    background-color: #1a73e8;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 18px;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background-color: #0f5fc4;
}
.download-btn>button {
    background-color:#34a853 !important;
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------
st.set_page_config(page_title="AI Resume Builder", layout="wide")

st.markdown("<div class='main-title'>📄 Intelligent Resume Builder</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Created by: Aditi Mishra • Lasit Vyas • Likith Kumar CR <br>Powered by LLM + n8n automation</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# Session state variables
# -------------------------------------------------------
if "final_pdf" not in st.session_state:
    st.session_state.final_pdf = None

# -------------------------------------------------------
# 1. Resume Section
# -------------------------------------------------------
st.header("1. Resume Section")

mode = st.radio("Select input method:", ["Upload Resume File", "Enter Manually"])

uploaded_file = None
manual_data = {}

if mode == "Upload Resume File":
    uploaded_file = st.file_uploader("📂 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    st.info("AI will extract and generate the missing information.")

else:
    st.subheader("Manual Entry")

    name = st.text_input("Full Name", key="name_input")
    title = st.text_input("Job Title", key="target_title")
    summary = st.text_area("Professional Summary (optional)", height=100, key="summary_input")

    st.subheader("Work Experience")
    exp_title = st.text_input("Experience - Job Title", key="exp_title")
    exp_company = st.text_input("Experience - Company Name", key="exp_company")
    exp_start = st.text_input("Experience - Start Year", key="exp_start")
    exp_end = st.text_input("Experience - End Year", key="exp_end")
    exp_bullets = st.text_area("Key Achievements (one per line)", key="exp_bullets")

    skills = st.text_input("Skills (comma separated)", key="skills_input")
    education = st.text_input("Education", key="education_input")
    contact = st.text_input("Contact (email or phone)", key="contact_input")

    manual_data = {
        "name": name,
        "title": title,
        "summary": summary,
        "education": education,
        "skills": skills,
        "contact": contact,
        "experience_text": f"{exp_title} at {exp_company} ({exp_start}-{exp_end})\n{exp_bullets}"
    }

# -------------------------------------------------------
# 2. Job Description Section
# -------------------------------------------------------
st.header("2. Job Description")

job_description = st.text_area("Paste the Job Description here:", height=180)

# -------------------------------------------------------
# 3. Generate Resume
# -------------------------------------------------------
if st.button("🚀 Generate My Resume"):

    if not job_description.strip():
        st.error("Job Description is required.")
        st.stop()

    if mode == "Upload Resume File" and not uploaded_file:
        st.error("Please upload a resume file first.")
        st.stop()

    st.info("Sending data to server...")

    # Build payload
    if mode == "Upload Resume File":
        file_bytes = uploaded_file.read()
        payload = {
            "mode": "upload",
            "filename": uploaded_file.name,
            "mime_type": uploaded_file.type,
            "data_base64": base64.b64encode(file_bytes).decode("utf-8"),
            "job_description": job_description
        }
    else:
        payload = {
            "mode": "manual",
            "job_description": job_description,
            **manual_data
        }

    # Call n8n
    try:
        resp = requests.post(N8N_WEBHOOK, json=payload, timeout=200)
        resp.raise_for_status()
        n8n_output = resp.json()
        st.write("DEBUG OUTPUT FROM N8N:", n8n_output)

        # URL returned by n8n
        final_url = (
            n8n_output.get("final_url") or 
            n8n_output.get("pdf_url") or 
            n8n_output.get("final_pdf_url")
        )

        if not final_url:
            st.error("❌ Server returned no PDF URL. Check your n8n workflow.")
            st.stop()

        st.session_state.final_pdf_url = final_url
        st.success("🎉 Resume Generated Successfully!")

    except Exception as e:
        st.error(f"Error contacting n8n: {e}")
        st.stop()


# -------------------------------------------------------
# 4. Download Section (PDF ONLY)
# -------------------------------------------------------
# -------------------------------------------------------
# 4. DOWNLOAD SECTION (URL-based PDF)
# -------------------------------------------------------
if st.session_state.get("final_pdf_url"):
    st.header("4. Download Your Resume")

    st.success("Your AI-optimized resume has been generated!")

    st.markdown(
        f"""
        <a href="{st.session_state.final_pdf_url}" target="_blank">
            <button style="
                background-color:#34a853;
                color:white;
                padding:12px 20px;
                border:none;
                border-radius:6px;
                font-size:18px;
                font-weight:600;
                cursor:pointer;">
                ⬇️ Download Resume (PDF)
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# Footer
st.markdown("<hr><center>Built with ❤️ by Our Group • Generative AI Final Project</center>", unsafe_allow_html=True)
