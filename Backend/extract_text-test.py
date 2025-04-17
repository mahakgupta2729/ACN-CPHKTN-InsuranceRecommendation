from extract_text import extract_text_from_pdf

# Replace this path with an actual PDF file you have
pdf_path = r"C:\Users\mahak.c.gupta\Downloads\Test_Report.pdf"

try:
    extracted = extract_text_from_pdf(pdf_path)
    print("✅ Extracted Text:\n")
    print(extracted)
except Exception as e:
    print("❌ Failed to extract text:")
    print(e)
