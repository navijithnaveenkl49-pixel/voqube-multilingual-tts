import traceback
try:
    import generate_abstract_pdf
    generate_abstract_pdf.create_pdf()
except Exception as e:
    with open('error_log_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(traceback.format_exc())
