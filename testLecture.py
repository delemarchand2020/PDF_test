import PyPDF2

# Open the PDF file
pdf_path = "C:/Users/delem/Downloads/Lemarchand-Paul_calques_on.pdf"
pdf_file = open(pdf_path, 'rb')

# Initialize PDF reader
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Get the total number of pages
num_pages = len(pdf_reader.pages)

# Extract text from each page
pdf_text = ""
for page_num in range(num_pages):
    page = pdf_reader.pages[page_num]
    pdf_text += f"-----------------{page_num}------------------\n"
    pdf_text += page.extract_text()

# Close the PDF file
pdf_file.close()

# Display the text extracted
print(pdf_text)
