import os, io, json, time, base64
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv
load_dotenv()

# Google Gemini
import google.generativeai as genai

# ============================================
# CONFIG
# ============================================
app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = "gemini-2.5-flash-lite"

model = None
model_loaded = False

# ============================================
# FALLBACK PROMPT
# ============================================
FALLBACK_PROMPT = """
You are an expert resume writer. Rewrite and enhance the following resume for ATS readability and professionalism.
Keep all facts. Improve clarity, structure, formatting, and action verbs.
Output MUST be valid HTML formatted resume.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY HTML, no explanations.
"""

# ============================================
# EXTRACT FILE TEXT
# ============================================
def extract_file_text(b64_data, mime_type, filename):
    try:
        file_bytes = base64.b64decode(b64_data)
    except:
        return "", "Invalid base64"

    try:
        if "pdf" in mime_type or filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        elif "word" in mime_type or filename.endswith(".docx"):
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            text = file_bytes.decode("utf-8", errors="ignore")

        return text.strip(), ""
    except Exception as e:
        return "", str(e)

# ============================================
# INIT MODEL
# ============================================
def load_model():
    global model, model_loaded
    try:
        print("Loading Gemini model...")

        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(MODEL_ID)

        model_loaded = True
        print("✅ Gemini 2.5 Flash-Lite loaded successfully")

    except Exception as e:
        print(f"❌ Failed to load Gemini model: {e}")
        model_loaded = False

# ============================================
# PREPARE PROMPT
# ============================================
def prepare_prompt(resume_text, job_description, custom_prompt):
    resume_limited = resume_text[:5000]
    job_limited = job_description[:3000]

    if custom_prompt:
        prompt = custom_prompt.replace("{resume_text}", resume_limited)
        prompt = prompt.replace("{job_description}", job_limited)
        return prompt

    return FALLBACK_PROMPT.format(
        resume_text=resume_limited,
        job_description=job_limited
    )

# ============================================
# GENERATE RESUME (HTML OUTPUT)
# ============================================
def generate_html_resume(resume_text, job_description, custom_prompt=""):
    if not model_loaded:
        return "ERROR: Model not loaded"

    try:
        prompt = prepare_prompt(resume_text, job_description, custom_prompt)

        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text.strip()

        return str(response)

    except Exception as e:
        return f"ERROR generating resume: {str(e)}"

# ============================================
# ENDPOINT: extract_text
# ============================================
@app.route("/extract_text", methods=["POST"])
def extract_text():
    try:
        data = request.get_json()
        filename = data.get("filename", "")
        mime_type = data.get("mime_type", "")
        b64_data = data.get("data_base64") or ""
        job_description = data.get("job_description", "")
        custom_prompt = data.get("prompt", "")

        # If user directly sends text
        if "resume_text" in data:
            return jsonify({
                "success": True,
                "resume_text": data["resume_text"],
                "job_description": job_description,
                "prompt": custom_prompt
            })

        if not b64_data:
            return jsonify({"error": "No file received"}), 400

        text, error = extract_file_text(b64_data, mime_type, filename)
        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "success": True,
            "resume_text": text,
            "job_description": job_description,
            "prompt": custom_prompt
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================
# ENDPOINT: generate_resume (returns HTML)
# ============================================
@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    try:
        data = request.get_json()

        resume_text = data.get("resume_text", "")
        job_description = data.get("job_description", "")
        custom_prompt = data.get("prompt", "")

        if not resume_text:
            return Response("resume_text missing", status=400)

        html_output = generate_html_resume(
            resume_text,
            job_description,
            custom_prompt
        )

        return Response(html_output, status=200, mimetype="text/html")

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

# ============================================
# test_prompt
# ============================================
@app.route("/test_prompt", methods=["POST"])
def test_prompt():
    data = request.get_json()
    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")
    custom_prompt = data.get("prompt", "")

    preview = prepare_prompt(resume_text, job_description, custom_prompt)

    return jsonify({
        "prompt_preview": preview[:400],
        "length": len(preview)
    })

# ============================================
# health
# ============================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model_loaded,
        "model": MODEL_ID
    })

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    load_model()
    print("\nServer running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
