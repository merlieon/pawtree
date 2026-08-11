from pypdf import PdfReader

reader = PdfReader("data/mudi.pdf")
print(f"Antal sidor: {len(reader.pages)}")


for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(text[:500])