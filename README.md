# CareerCraft AI - Intelligent Resume Optimization System

## 🎯 Project Overview

CareerCraft AI is an intelligent, end-to-end resume optimization system designed to help students and job seekers create professional, ATS-optimized resumes tailored to specific job descriptions. Built with modern AI technologies and automation workflows, this system transforms poorly formatted resumes into compelling, keyword-rich documents that pass through Applicant Tracking Systems (ATS) and catch recruiters' attention.

**Problem Solved:** Many qualified candidates get rejected due to poor resume formatting, missing ATS keywords, and lack of personalization for different job roles. CareerCraft AI automates the entire resume enhancement process using Generative AI while maintaining accuracy, clarity, and professional formatting.

## 👥 Contributors

This project was developed by:
- **Likithkumar CR**
- **Lasit Vyas** 
- **Aditi Mishra**

Under the guidance of Prof. Onur Barut at Clark University.

## 🚀 Key Features

- **Dual Input Modes**: Upload existing resume (PDF/DOCX) or enter details manually
- **AI-Powered Enhancement**: Fine-tuned language model rewrites weak bullet points with quantified achievements
- **ATS Optimization**: Automatically includes relevant keywords from job descriptions
- **Professional Formatting**: Generates clean, print-ready PDF resumes
- **Fast Processing**: Complete resume transformation in minutes
- **Multiple Template Support**: Various professional templates available

## 🛠️ Technology Stack

### Core Technologies
- **Frontend**: Streamlit - Clean, intuitive web interface
- **Workflow Automation**: n8n - Orchestrates backend processes
- **AI Model**: Gemini Flash 2.5- Lite
- **Document Processing**: Flask microservice with PyPDF2 & python-docx
- **PDF Generation**: HTML/CSS to PDF conversion
- **Model Hosting**: Hugging Face Inference API

### Development Tools
- **Model Fine-tuning**: LoRA (Low-Rank Adaptation) + 4-bit Quantization (Microsoft Phi-3 Mini 4k)
- **Deployment**: ngrok for development, Azure-ready architecture
- **Programming Languages**: Python, JavaScript
- **Version Control**: Git & GitHub

## 📋 System Architecture

1. **User Interface**: Streamlit frontend for resume upload/job description input
2. **Workflow Engine**: n8n coordinates file processing, AI inference, and document generation
3. **Extraction Service**: Flask microservice extracts text from PDF/DOCX files
4. **AI Enhancement**: Fine-tuned Phi-3 model rewrites and optimizes resume content
5. **Document Generator**: Creates professional PDF from enhanced HTML content

## 🎯 Use Cases

- **Students & Recent Graduates**: Create first professional resume
- **Job Seekers**: Tailor resumes for specific job applications
- **Career Changers**: Reposition skills for new industries
- **International Applicants**: Adapt resumes to regional standards
- **University Career Centers**: Deploy as institutional resource

## 📊 Results & Impact

- **Quality Improvement**: Transforms generic statements into quantified achievements
- **Time Efficiency**: Reduces resume creation time from hours to minutes
- **ATS Success**: Significantly improves automated screening pass rates
- **Consistency**: Maintains professional formatting across all outputs
- **Scalability**: Lightweight model delivers high performance at low cost

## 🔧 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/aditimishra28/airesumeportfoliobuilder
cd airesumeportfoliobuilder

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configurations

# Run the application
streamlit run app.py
```

## 📖 Usage

1. **Upload Resume**: Drag and drop your PDF/DOCX resume or enter details manually
2. **Add Job Description**: Paste the target job description
3. **Generate**: Click "Generate My Resume" 
4. **Download**: Receive your optimized, ATS-friendly resume in PDF format

## 📄 Citation & Usage Policy

If you use CareerCraft AI in your research, projects, or applications, please cite:

```bibtex
@software{career_craft_ai_2024,
  title={CareerCraft AI: Intelligent Resume Optimization System Using Generative AI},
  author={CR, Likithkumar and Vyas, Lasit and Mishra, Aditi},
  year={2024},
  publisher={Clark University},
  url={https://github.com/aditimishra28/airesumeportfoliobuilder}
}
```

**Citation Requirements:**
- Academic papers or publications
- Commercial applications
- Derivative works or forks
- Presentations or demos
- Any public use of the codebase



**⭐ Star this repository if you find it helpful!**
