from fpdf import FPDF
import os

class ArchitecturePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, 'VoQube - System Design and Architecture', ln=True, align='C')
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Detailed Technical Breakdown', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(20, 20, 20)
        # Using multi_cell to handle line breaks correctly
        # Encoding issues can occur with fpdf, so encode/decode or stick to safe characters.
        body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, body)
        self.ln(5)

    def chapter_sub_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, ln=True, align='L')
        self.ln(1)


def create_pdf():
    pdf = ArchitecturePDF()
    pdf.add_page()

    # 1. Functional Overview
    pdf.chapter_title("1. Functional Overview & Capabilities")
    pdf.chapter_body(
        "VoQube is designed to provide high-fidelity, neural voice synthesis. It does not rely on basic, "
        "robotic fallback voices; instead, it hooks into cloud-level AI architectures to provide streaming-quality "
        ".mp3 exports.\n\n"
        "Key Technical Capabilities:\n"
        "- Neural Voice Synthesis (edge-tts): Uses Microsoft Edge TTS for high-quality, human-sounding 'Neural' voices.\n"
        "- Deep Translation API: Before synthesis, text is passed through deep_translator. English can be "
        "automatically converted to target languages before passing to the speech engine.\n"
        "- Asynchronous Processing: FastAPI routes are strictly asynchronous (async def) for non-blocking file "
        "generation and translation.\n"
        "- Dynamic Role-Based Access (RBAC): Admins have unrestricted bounds, whereas standard users are limited "
        "by tokens.\n"
        "- Persistence: Audio is written to a secure directory (/storage/audio) and serialized via static mounts."
    )

    # 2. Backend Architecture
    pdf.chapter_title("2. Deep Dive: Backend Architecture (FastAPI & Python)")
    pdf.chapter_body(
        "The Server is organized around micro-service philosophy:\n\n"
        "Entry & Routing (main.py):\n"
        "The core API router. Handles CORS and mounts the /storage/audio directory to /static/audio. "
        "Maps endpoints like /api/tts/generate and /api/admin/*.\n\n"
        "Database Schema (models.py):\n"
        "Uses SQLAlchemy to define mapping to MySQL.\n"
        "- Users Table: Tracks username, email, hashed password, role, and free generations.\n"
        "- Sessions Table: Monitors active API JSON Web Tokens.\n"
        "- VoiceGeneration Table: Records generated text, translated text, voice type, language, and file path.\n"
        "- Download Table: Tracks user download metrics tied to specific generations.\n\n"
        "TTS Service Engine (tts_service.py):\n"
        "Maintains mappings for 10+ languages to AI Voice Strings. Generates UUID-v4 hashes for files "
        "to prevent overwrite collisions."
    )

    # 3. Frontend UI Architecture
    pdf.chapter_title("3. Deep Dive: Frontend UI Architecture (React & Vite)")
    pdf.chapter_body(
        "The front-end is structured as a SPA rendering via App.jsx and styling via a custom MUI theme.js.\n\n"
        "Page Layouts (src/pages/):\n"
        "- Login.jsx & Register.jsx: Handles the JWT OAuth token handshaking.\n"
        "- Layout.jsx: Persistent layout wrapper spanning sidebar and top nav.\n"
        "- Dashboard.jsx: The user control center for inputting script, toggling auto-translate, and triggering "
        "speech generation. Updates token wallet immediately.\n"
        "- History.jsx: Private view parsing /api/tts/history to display table rows of past generations.\n"
        "- AdminPanel.jsx: Protected UI rendering aggregate system analytics and token management tool limits."
    )

    # 4. System Lifecycle Example
    pdf.chapter_title("4. Step-By-Step System Lifecycle Example")
    pdf.chapter_body(
        "1. Client-Side: User enters text on Dashboard, selects Language and Voice, and triggers Generate.\n"
        "2. Auth Network: Axios attaches JWT token to the Headers and sends JSON.\n"
        "3. Server Integrity: FastAPI decodes the token, checks 'Users' table for token balance.\n"
        "4. Translation thread: tts_service translates the text if required.\n"
        "5. Synthesis: Script instructs edge-tts to read text and stream to .mp3.\n"
        "6. Database Commit: Creates a VoiceGenerations row and deducts token from the User.\n"
        "7. Client Render: Sends back file path. The React Dashboard renders the Audio HTML5 Player."
    )

    output_path = "VoQube_Architecture_Detailed.pdf"
    pdf.output(output_path)
    print(f"PDF successfully generated: {output_path}")

if __name__ == '__main__':
    create_pdf()
