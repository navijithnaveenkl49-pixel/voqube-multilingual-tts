from fpdf import FPDF

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    with open('Detailed_Project_Abstract.md', 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('**', '')

    for line in text.split('\n'):
        # Ensure only ascii characters are processed
        line_clean = line.encode('ascii', 'ignore').decode('ascii')
        if line.startswith('# '):
            pdf.set_font('Helvetica', 'B', 18)
            pdf.multi_cell(190, 10, txt=line_clean[2:])
            pdf.ln(4)
        elif line.startswith('## '):
            pdf.set_font('Helvetica', 'B', 14)
            pdf.multi_cell(190, 8, txt=line_clean[3:])
            pdf.ln(3)
        elif line.startswith('- '):
            pdf.set_font('Helvetica', '', 11)
            pdf.multi_cell(190, 6, txt="  * " + line_clean[2:])
        elif line.strip() == '':
            pdf.ln(2)
        else:
            pdf.set_font('Helvetica', '', 11)
            if line_clean.strip():
                pdf.multi_cell(190, 6, txt=line_clean)

    output_path = 'Detailed_Project_Abstract.pdf'
    pdf.output(output_path)
    print(f"Successfully created {output_path}")

if __name__ == "__main__":
    create_pdf()
