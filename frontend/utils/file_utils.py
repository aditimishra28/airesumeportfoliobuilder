import io
import json
import zipfile
from pathlib import Path
from docxtpl import DocxTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER

BASE_DIR = Path(__file__).resolve().parents[1]
RESUME_TEMPLATE = BASE_DIR / "templates" / "resume_template.docx"
COVER_LETTER_TEMPLATE = BASE_DIR / "templates" / "cover_letter_template.docx"
PORTFOLIO_TEMPLATE = BASE_DIR / "templates" / "portfolio_template.html"
PORTFOLIO_STYLE = BASE_DIR / "templates" / "style.css"


# ==========================================
# 1. BUILD PLAIN TEXT RESUME (for PDF)
# ==========================================
def build_text_resume(data):
    lines = []

    # Header
    if "name" in data: lines.append(data["name"])
    if "title" in data: lines.append(data["title"])
    lines.append("")

    # Summary
    if data.get("summary"):
        lines.append("SUMMARY:")
        lines.append(data["summary"])
        lines.append("")

    # Experience
    lines.append("EXPERIENCE:")
    for exp in data.get("experiences", []):
        lines.append(f"{exp.get('title','')} — {exp.get('company','')} ({exp.get('start','')}–{exp.get('end','')})")
        for bullet in exp.get("bullets", []):
            lines.append(f"• {bullet}")
        lines.append("")

    # Skills
    if "skills" in data:
        lines.append("SKILLS:")
        if isinstance(data["skills"], list):
            lines.append(", ".join(data["skills"]))
        else:
            lines.append(data["skills"])
        lines.append("")

    # Education
    if "education" in data:
        lines.append("EDUCATION:")
        lines.append(data["education"])
        lines.append("")

    return "\n".join(lines)


# ==========================================
# 2. DOCX RESUME GENERATOR
# ==========================================
def generate_docx_bytes(structured_data):
    doc = DocxTemplate(RESUME_TEMPLATE)
    doc.render(structured_data)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# 3. UNIVERSAL PDF GENERATOR (TEXT → PDF)
# ==========================================
def generate_pdf_from_text(text: str) -> bytes:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# 4. COVER LETTER (DOCX)
# ==========================================
def generate_cover_letter(data):
    doc = DocxTemplate(COVER_LETTER_TEMPLATE)
    doc.render(data)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# 5. PORTFOLIO ZIP BUILDER
# ==========================================
def generate_portfolio_zip_bytes(structured_data):
    html_template = PORTFOLIO_TEMPLATE.read_text()
    style_css = PORTFOLIO_STYLE.read_text()

    # Convert experiences to readable text
    experiences_text = ""
    for exp in structured_data.get("experiences", []):
        experiences_text += f"{exp['title']} at {exp['company']} ({exp['start']}–{exp['end']})\n"
        for b in exp.get("bullets", []):
            experiences_text += f"• {b}\n"
        experiences_text += "\n"

    filled_html = html_template.format(
        name=structured_data.get("name", ""),
        summary=structured_data.get("summary", ""),
        skills=", ".join(structured_data.get("skills", [])),
        education=structured_data.get("education", ""),
        experiences=experiences_text
    )

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("index.html", filled_html)
        zf.writestr("style.css", style_css)

    buffer.seek(0)
    return buffer.getvalue()
