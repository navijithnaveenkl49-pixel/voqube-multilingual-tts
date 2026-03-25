from fpdf import FPDF

class ReferencesPDF(FPDF):
    def header(self):
        # Empty header as in the image there is only a title on the page, no repeating header
        pass

    def footer(self):
        # The image doesn't show a footer, maybe page number if needed
        self.set_y(-15)
        self.set_font('Times', '', 10)
        self.cell(0, 10, f'{self.page_no()}', align='C')

def create_references_pdf():
    pdf = ReferencesPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.ln(20) # Add some top margin

    # Title
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 10, 'REFERENCES', ln=True, align='C')
    pdf.ln(10)

    references = [
        {
            "title": "FastAPI Official Documentation",
            "link": "https://fastapi.tiangolo.com/",
            "usage": "(Used for backend development, API routing, and asynchronous request handling.)"
        },
        {
            "title": "React Official Documentation",
            "link": "https://react.dev/",
            "usage": "(Used for building the interactive, component-based user interface.)"
        },
        {
            "title": "Material UI (MUI) Documentation",
            "link": "https://mui.com/",
            "usage": "(Used for applying premium, responsive styling and pre-built React components.)"
        },
        {
            "title": "Google Text-to-Speech (gTTS) Library",
            "link": "https://gtts.readthedocs.io/",
            "usage": "(Used as a core synthesis engine for generating audio from text.)"
        },
        {
            "title": "Vite Official Documentation",
            "link": "https://vitejs.dev/",
            "usage": "(Used for fast frontend build processing and development server hosting.)"
        },
        {
            "title": "MySQL Official Documentation",
            "link": "https://dev.mysql.com/doc/",
            "usage": "(Used as a reference for database storage, state management, and user data persistence.)"
        },
        {
            "title": "SQLAlchemy Official Documentation",
            "link": "https://docs.sqlalchemy.org/",
            "usage": "(Used as the Object-Relational Mapper (ORM) for secure database interactions.)"
        }
    ]

    # Render references
    current_num = 1
    for ref in references:
        # Number and Title
        pdf.set_font('Times', '', 12)
        pdf.set_text_color(0, 0, 0) # Black
        
        pdf.cell(10, 6, f"{current_num}.", align='R')
        pdf.cell(2, 6, "") # Gap
        pdf.cell(0, 6, ref['title'], ln=True)
        
        # Link in Blue, underlined
        pdf.set_font('Times', 'U', 12)
        pdf.set_text_color(0, 0, 255) # Blue
        pdf.set_x(pdf.l_margin + 12) # Align with text
        pdf.cell(0, 6, ref['link'], ln=True, link=ref['link'])
        
        # Usage
        pdf.set_font('Times', '', 12)
        pdf.set_text_color(0, 0, 0) # Black
        pdf.set_x(pdf.l_margin + 12)
        pdf.multi_cell(0, 6, ref['usage'])
        
        pdf.ln(4) # Space between references
        current_num += 1

    # Book references like in the image
    pdf.set_font('Times', '', 12)
    pdf.set_text_color(0, 0, 0) # Black
    
    # 8. Web Development Textbook
    pdf.cell(10, 6, f"{current_num}.", align='R')
    pdf.cell(2, 6, "")
    pdf.cell(0, 6, "Web Development Architecture", ln=True)
    
    # Item 'o'
    pdf.set_font('Times', '', 12)
    pdf.set_x(pdf.l_margin + 18)
    pdf.cell(5, 6, "o")
    # Using italic for the book title
    pdf.multi_cell(0, 6, "MDN Web Docs (Mozilla Developer Network), HTML, CSS, and API Reference, Mozilla Foundation.")
    pdf.ln(4)
    current_num += 1

    # 9. Software Engineering
    pdf.set_font('Times', '', 12)
    pdf.cell(10, 6, f"{current_num}.", align='R')
    pdf.cell(2, 6, "")
    pdf.cell(0, 6, "Software Engineering Principles", ln=True)
    
    # Item 'o'
    pdf.set_x(pdf.l_margin + 18)
    pdf.cell(5, 6, "o")
    pdf.multi_cell(0, 6, "Ian Sommerville, Software Engineering, Pearson Education.")
    pdf.ln(4)

    output_path = "VoQube_References.pdf"
    pdf.output(output_path)
    print(f"PDF successfully generated: {output_path}")

if __name__ == "__main__":
    create_references_pdf()
