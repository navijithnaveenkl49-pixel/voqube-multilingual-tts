import os
from fpdf import FPDF

class TechStackPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(99, 102, 241)
        self.cell(0, 10, 'VoQube - Tech Stack and Source Code Report', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 6, body)
        self.ln(5)

    def add_code_snippet(self, code_text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        safe_text = code_text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 5, safe_text, fill=True)
        self.ln(5)

def generate_report():
    pdf = TechStackPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 24)
    pdf.ln(50)
    pdf.cell(0, 10, 'TECH STACK & SOURCE CODE REPORT', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 10, 'VoQube: Multilingual Text-to-Speech Generator', ln=True, align='C')
    pdf.ln(30)
    
    # Tech Stack Overview
    pdf.add_page()
    pdf.chapter_title("1. Tech Stack Overview")
    overview = (
        "VoQube is built using a modern, scalable tech stack:\n\n"
        "- Frontend: React.js, Vite, Material UI (MUI)\n"
        "- Backend: FastAPI, SQLAlchemy, Pydantic, Python 3.8+\n"
        "- Database (DBMS): MySQL 8.0+\n"
        "- Audio Processing: gTTS (Google Text-to-Speech) / Edge-TTS\n\n"
        "This architectural choice ensures a robust, high-performance experience "
        "for users, capable of handling rapid text-to-speech generation requests "
        "while maintaining a responsive user interface."
    )
    pdf.chapter_body(overview)
    
    # Sections and files to include
    sections = [
        ("2. Frontend Code", ["frontend/src/App.jsx", "frontend/src/main.jsx", "frontend/src/theme.js", "frontend/index.html"]),
        ("3. Backend Code", ["backend/main.py", "backend/tts_service.py", "backend/auth_utils.py"]),
        ("4. DBMS Code", ["backend/database.py", "backend/models.py", "backend/schemas.py"])
    ]
    
    for section_title, files in sections:
        pdf.add_page()
        pdf.chapter_title(section_title)
        
        for file_path in files:
            if not os.path.exists(file_path):
                # Check root directory if not in subfolder
                root_path = os.path.basename(file_path)
                if os.path.exists(root_path):
                    file_path = root_path
                else:
                    continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_text = f.read()
                
                if not code_text.strip():
                    continue
                
                pdf.set_font('Helvetica', 'B', 12)
                pdf.cell(0, 10, f"File: {file_path}", ln=True)
                
                # chunk the code to not make multi_cell too big at once
                chunks = [code_text[i:i+4000] for i in range(0, len(code_text), 4000)]
                for chunk in chunks:
                    pdf.add_code_snippet(chunk)
                    
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    output_filename = 'VoQube_TechStack_Report.pdf'
    pdf.output(output_filename)
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    generate_report()
