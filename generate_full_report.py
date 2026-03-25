"""
VoQube Full Project Report Generator
Reads actual source files and embeds them in PDF using reportlab for better Unicode support.
Falls back to fpdf2 if reportlab not available.
"""
import os
import sys

# Try reportlab first (better Unicode handling)
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Preformatted, PageBreak, Table, TableStyle)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    USE_REPORTLAB = True
    print("Using reportlab")
except ImportError:
    USE_REPORTLAB = False
    print("reportlab not found, using fpdf2")


BASE = r"c:\Users\sindh\Desktop\text to speech generator"

# Map of sections -> list of (label, filepath)
SECTIONS = [
    ("2. Frontend Code",  [
        ("2.1 Login Page",             "frontend/src/pages/Login.jsx"),
        ("2.2 Sign Up / Register Page","frontend/src/pages/Register.jsx"),
        ("2.3 User Dashboard Panel",   "frontend/src/pages/Dashboard.jsx"),
        ("2.4 User Generation History","frontend/src/pages/History.jsx"),
        ("2.5 Admin Dashboard / Control Panel","frontend/src/pages/AdminPanel.jsx"),
        ("2.6 Layout / Sidebar Navigation",    "frontend/src/components/Layout.jsx"),
    ]),
    ("3. Backend Code", [
        ("3.1 Main API (main.py)",       "backend/main.py"),
        ("3.2 Auth Utilities",           "backend/auth_utils.py"),
        ("3.3 TTS and Translation Service","backend/tts_service.py"),
    ]),
    ("4. DBMS Code (MySQL / SQLAlchemy)", [
        ("4.1 Database Connection",      "backend/database.py"),
        ("4.2 ORM Models / Table Schemas","backend/models.py"),
        ("4.3 Pydantic Schemas",         "backend/schemas.py"),
    ]),
]

TECH_STACK_TEXT = """\
VoQube is a full-stack SaaS application for multilingual text-to-speech generation.
The system is divided into three major layers:

  FRONTEND  : React.js + Vite + Material UI (MUI)
  BACKEND   : FastAPI (Python) + SQLAlchemy + PyJWT + bcrypt + Edge-TTS
  DATABASE  : MySQL 8.0 (accessed via SQLAlchemy ORM)

Key Libraries and Tools:
  - edge-tts         : Microsoft Azure neural voice synthesis
  - deep-translator  : Google Translate integration
  - bcrypt           : Secure password hashing
  - PyJWT            : JSON Web Token authentication
  - react-router-dom : Client-side SPA routing
  - axios            : HTTP client for API calls
  - Material UI      : React component library

Architecture Pattern:
  REST API backend + Single Page Application (SPA) frontend.
  JWT Bearer tokens stored in localStorage for session management.
  Audio files stored on filesystem (storage/audio/*.mp3) served as static files.

Database Tables:
  users             -- user accounts (id, username, email, hashed_password, role, tokens)
  sessions          -- active JWT sessions per user
  voice_generations -- each TTS output (text, language, voice, file path, timestamp)
  downloads         -- tracks every audio download event
"""

SQL_SCHEMA = """\
-- ============================================================
-- VoQube MySQL Database Schema (equivalent DDL)
-- ============================================================
CREATE DATABASE IF NOT EXISTS voqube
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE voqube;

-- Users table
CREATE TABLE users (
    id                    INT          AUTO_INCREMENT PRIMARY KEY,
    username              VARCHAR(50)  NOT NULL UNIQUE,
    email                 VARCHAR(100) NOT NULL UNIQUE,
    hashed_password       VARCHAR(255) NOT NULL,
    role                  VARCHAR(20)  NOT NULL DEFAULT 'user',
    free_generations_left INT          NOT NULL DEFAULT 10,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email    (email)
);

-- Sessions table (JWT tokens)
CREATE TABLE sessions (
    id           INT          AUTO_INCREMENT PRIMARY KEY,
    user_id      INT          NOT NULL,
    active_token VARCHAR(500) NOT NULL,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_active_token (active_token),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Voice generations table
CREATE TABLE voice_generations (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    user_id         INT          NOT NULL,
    text            TEXT         NOT NULL,
    translated_text TEXT,
    language        VARCHAR(50)  NOT NULL,
    voice_type      VARCHAR(50)  NOT NULL,
    file_path       VARCHAR(255) NOT NULL,
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Downloads tracking table
CREATE TABLE downloads (
    id            INT      AUTO_INCREMENT PRIMARY KEY,
    user_id       INT      NOT NULL,
    generation_id INT      NOT NULL,
    download_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (generation_id)
        REFERENCES voice_generations(id) ON DELETE CASCADE
);

-- Admin stats queries
SELECT COUNT(*) AS total_users        FROM users;
SELECT COUNT(*) AS total_generations  FROM voice_generations;
SELECT COUNT(*) AS total_downloads    FROM downloads;

-- User history query (by user_id)
SELECT * FROM voice_generations
WHERE user_id = ?
ORDER BY created_at DESC;

-- Admin: full user list
SELECT id, username, email, role, free_generations_left, created_at
FROM users;
"""


def safe(text):
    """Replace non-latin-1 chars safely."""
    return text.encode('latin-1', 'replace').decode('latin-1')


def wrap_code(text, width=90):
    """Wrap long lines so fpdf doesn't crash."""
    lines = []
    for line in text.splitlines():
        while len(line) > width:
            lines.append(line[:width])
            line = '    ' + line[width:]
        lines.append(line)
    return '\n'.join(lines)


def read_file(rel_path):
    full = os.path.join(BASE, rel_path.replace('/', os.sep))
    try:
        with open(full, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"# [Error reading file: {e}]"


# ============================================================
# REPORTLAB VERSION (preferred)
# ============================================================
def generate_with_reportlab():
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.enums import TA_CENTER

    outfile = os.path.join(BASE, 'VoQube_Full_TechStack_Report.pdf')
    doc = SimpleDocTemplate(outfile, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title2', parent=styles['Title'],
                                 fontSize=26, textColor=colors.HexColor('#6366f1'),
                                 spaceAfter=10, alignment=TA_CENTER)
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
                              fontSize=16, textColor=colors.HexColor('#6366f1'),
                              spaceBefore=12, spaceAfter=6,
                              borderPad=4, backColor=colors.HexColor('#f0eeff'))
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
                              fontSize=13, textColor=colors.HexColor('#1e293b'),
                              spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle('Body2', parent=styles['Normal'],
                                fontSize=10, leading=15, spaceAfter=8)
    code_style = ParagraphStyle('Code', parent=styles['Code'],
                                fontSize=7.5, fontName='Courier',
                                leading=11, backColor=colors.HexColor('#f2f2fa'),
                                spaceBefore=4, spaceAfter=8,
                                leftIndent=6, rightIndent=6)
    file_hdr_style = ParagraphStyle('FileHdr', parent=styles['Normal'],
                                    fontName='Helvetica-Bold', fontSize=10,
                                    textColor=colors.white,
                                    backColor=colors.HexColor('#3c3c8c'),
                                    leftIndent=6, spaceBefore=6, spaceAfter=2)

    story = []

    # Title page
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("VoQube", title_style))
    story.append(Paragraph("Multilingual Text-to-Speech Generator", ParagraphStyle(
        'sub', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER,
        textColor=colors.HexColor('#1e293b'), spaceAfter=8)))
    story.append(Paragraph("Complete Project Report", ParagraphStyle(
        'sub2', parent=styles['Normal'], fontSize=13, alignment=TA_CENTER,
        textColor=colors.HexColor('#6060aa'), spaceAfter=4)))
    story.append(Paragraph("Tech Stack | Login Page | Sign Up | User Panel | History | Admin Dashboard | DBMS", ParagraphStyle(
        'sub3', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER,
        textColor=colors.HexColor('#888'), spaceAfter=30)))
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Department of Computer Science and Engineering", ParagraphStyle(
        'dept', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER,
        textColor=colors.HexColor('#888'))))
    story.append(Paragraph("Bachelor of Technology  |  Final Year Project", ParagraphStyle(
        'dept2', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER,
        textColor=colors.HexColor('#888'))))
    story.append(PageBreak())

    # Tech Stack Overview
    story.append(Paragraph("1. Tech Stack Overview", h1_style))
    for line in TECH_STACK_TEXT.strip().split('\n'):
        story.append(Paragraph(line if line.strip() else '&nbsp;', body_style))
    story.append(PageBreak())

    # All sections
    for section_title, files in SECTIONS:
        story.append(Paragraph(section_title, h1_style))
        story.append(Spacer(1, 4*mm))

        for file_label, file_path in files:
            code = read_file(file_path)
            story.append(Paragraph(f"{file_label}  ({file_path})", h2_style))
            story.append(Paragraph(f"File: {file_path}", file_hdr_style))
            # In reportlab Preformatted handles long lines by truncating, so we wrap manually
            wrapped = wrap_code(code, width=100)
            story.append(Preformatted(wrapped, code_style))
            story.append(Spacer(1, 6*mm))

        story.append(PageBreak())

    # Extra DBMS: raw SQL
    story.append(Paragraph("4.4  Equivalent MySQL DDL Statements", h2_style))
    for line in [
        "The following SQL represents the schema that SQLAlchemy auto-creates.",
        "You can run these statements in MySQL Workbench to set up the database manually."
    ]:
        story.append(Paragraph(line, body_style))
    story.append(Paragraph("File: schema.sql  --  MySQL DDL", file_hdr_style))
    story.append(Preformatted(wrap_code(SQL_SCHEMA, 100), code_style))

    doc.build(story)
    print(f"SUCCESS: VoQube_Full_TechStack_Report.pdf generated!")


# ============================================================
# FPDF2 FALLBACK VERSION
# ============================================================
def generate_with_fpdf():
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(99, 102, 241)
            self.cell(0, 8, safe('VoQube - Full Project Report (Tech Stack, Code and DBMS)'),
                      new_x='LMARGIN', new_y='NEXT', align='C')
            self.set_draw_color(99, 102, 241)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(3)

        def footer(self):
            self.set_y(-13)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(130, 130, 130)
            self.cell(0, 8, safe(f'Page {self.page_no()}  |  VoQube - Multilingual TTS Generator'), align='C')

        def sec(self, title):
            self.set_font('Helvetica', 'B', 13)
            self.set_text_color(99, 102, 241)
            self.set_fill_color(240, 238, 255)
            self.cell(0, 9, safe(title), new_x='LMARGIN', new_y='NEXT', fill=True)
            self.ln(2)

        def sub(self, title):
            self.set_font('Helvetica', 'B', 11)
            self.set_text_color(30, 41, 59)
            self.cell(0, 8, safe(title), new_x='LMARGIN', new_y='NEXT')
            self.ln(1)

        def body(self, text):
            self.set_font('Helvetica', '', 10)
            self.set_text_color(50, 60, 80)
            self.multi_cell(0, 6, safe(text))
            self.ln(3)

        def fhdr(self, label):
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(255, 255, 255)
            self.set_fill_color(60, 60, 140)
            self.cell(0, 7, safe(f'  {label}'), new_x='LMARGIN', new_y='NEXT', fill=True)
            self.ln(1)

        def code(self, text):
            self.set_font('Courier', '', 8)
            self.set_fill_color(242, 242, 250)
            self.set_text_color(20, 20, 60)
            wrapped = wrap_code(safe(text), width=88)
            for chunk in [wrapped[i:i+2500] for i in range(0, len(wrapped), 2500)]:
                self.multi_cell(0, 4.5, chunk, fill=True)
            self.ln(4)

    pdf = PDF()
    pdf.set_margins(left=15, top=22, right=15)
    pdf.set_auto_page_break(auto=True, margin=18)

    # Title page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(99, 102, 241)
    pdf.ln(40)
    pdf.cell(0, 12, 'VoQube', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 9, 'Multilingual Text-to-Speech Generator', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(80, 80, 120)
    pdf.cell(0, 7, 'Complete Project Report', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 7, 'Tech Stack | Source Code | DBMS Schema', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 100, 140)
    pdf.cell(0, 7, 'Department of Computer Science and Engineering', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 7, 'Bachelor of Technology  |  Final Year Project', new_x='LMARGIN', new_y='NEXT', align='C')

    # Tech stack
    pdf.add_page()
    pdf.sec('1. Tech Stack Overview')
    for line in TECH_STACK_TEXT.strip().split('\n'):
        pdf.body(line)

    # Sections
    for section_title, files in SECTIONS:
        pdf.add_page()
        pdf.sec(section_title)
        for file_label, file_path in files:
            code = read_file(file_path)
            pdf.sub(file_label)
            pdf.fhdr(f'File: {file_path}')
            pdf.code(code)

    # SQL Schema
    pdf.add_page()
    pdf.sec('4.4  Equivalent MySQL DDL Statements')
    pdf.body('The following SQL represents the schema created by SQLAlchemy.')
    pdf.body('Run these in MySQL Workbench to set up the voqube database manually.')
    pdf.fhdr('File: schema.sql  --  MySQL DDL')
    pdf.code(SQL_SCHEMA)

    out = os.path.join(BASE, 'VoQube_Full_TechStack_Report.pdf')
    pdf.output(out)
    print(f"SUCCESS: VoQube_Full_TechStack_Report.pdf generated with {pdf.page_no()} pages!")


if __name__ == '__main__':
    # Install reportlab if possible
    try:
        import reportlab
        USE_REPORTLAB = True
    except ImportError:
        USE_REPORTLAB = False

    if USE_REPORTLAB:
        generate_with_reportlab()
    else:
        generate_with_fpdf()
