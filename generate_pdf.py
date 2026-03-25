from fpdf import FPDF

class AbstractPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(99, 102, 241)  # VoQube Indigo
        self.cell(0, 15, 'VoQube - Multilingual TTS Generator', ln=True, align='C')
        self.set_font('Helvetica', 'I', 12)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, 'Project Abstract & Technical Overview', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()} | VoQube Research & Development', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(168, 85, 247)  # Purple Accent
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 7, body)
        self.ln(5)

def create_voqube_pdf():
    pdf = AbstractPDF()
    pdf.add_page()
    
    # Abstract Section
    pdf.chapter_title("Abstract")
    abstract_text1 = (
        "VoQube is a sophisticated, high-performance Multilingual Text-to-Speech (TTS) generator "
        "designed to meet the growing demand for high-quality synthetic voice content in gaming, "
        "streaming, and digital creation. The platform leverages advanced speech synthesis engines, "
        "such as gTTS and Edge-TTS, to provide users with natural-sounding vocal outputs across a "
        "wide array of regional Indian and international languages."
    )
    pdf.chapter_body(abstract_text1)
    
    abstract_text2 = (
        "Built with a modern architectural stack consisting of a FastAPI backend and a React-driven "
        "frontend, VoQube offers a seamless, real-time experience. The system integrates a robust "
        "Token-Based Economy, allowing administrators to manage user access and generation limits "
        "through a dedicated Admin Panel. This ensures scalability and controlled resource allocation "
        "while providing a streamlined interface for end-users to generate, track, and download their "
        "speech history."
    )
    pdf.chapter_body(abstract_text2)
    
    # Key Features
    pdf.chapter_title("Key Features")
    features = [
        "Multilingual Synthesis: Support for diverse languages with selectable voice profiles (Male/Female).",
        "Administrative Control: Centralized dashboard for token adjustments and usage monitoring.",
        "Modern User Experience: Premium, responsive UI built with Material UI (MUI) and Vite.",
        "Data Persistence: Secure MySQL backend for user profiles and generation metadata."
    ]
    for feature in features:
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(10)
        pdf.cell(0, 7, f"- {feature}", ln=True)
    pdf.ln(10)
    
    # Tech Stack
    pdf.chapter_title("Technical Stack")
    tech_stack = "FastAPI, React.js, Vite, MySQL, gTTS, Edge-TTS, Material UI, Pydantic"
    pdf.chapter_body(tech_stack)
    
    pdf.output("VoQube_Abstract.pdf")
    print("PDF generated successfully: VoQube_Abstract.pdf")

if __name__ == "__main__":
    create_voqube_pdf()
