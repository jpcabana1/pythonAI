import PyPDF2
import os
from io import BytesIO

def bytes_to_mb(byte_size):
    # 1 MB = 2^20 bytes = 1048576 bytes
    return byte_size / (1024 * 1024)

def get_pdf_size_in_bytes(writer):
    # Create a BytesIO object to hold the PDF data
    pdf_bytes = BytesIO()
    # Write the PDF content to the BytesIO object
    writer.write(pdf_bytes)
    # Get the size of the BytesIO object
    pdf_size = pdf_bytes.tell()
    return pdf_size

def pdf_split(input_pdf_path, output_dir, page_size, maximum_file_size):
    with open(input_pdf_path, 'rb') as input_pdf:
        reader_pdf = PyPDF2.PdfReader(input_pdf)

        num_pages = len(reader_pdf.pages)
        
        for page_index in range(0, len(reader_pdf.pages), page_size):
            #print(f"index={page_index}, index+{page_size}={min(page_index+page_size, num_pages)}")
        
            writer_pdf = PyPDF2.PdfWriter()
            for page in range(page_index, min(page_index + page_size, num_pages)):
                writer_pdf.add_page(reader_pdf.pages[page])
                    
            writer_size_in_mb = round(bytes_to_mb(get_pdf_size_in_bytes(writer_pdf)), 2)
            if writer_size_in_mb > maximum_file_size:
                print(f" page {page_index} to {min(page_index + page_size, num_pages)} has {writer_size_in_mb}mb.")
                    
            output_pdf_path = f"{output_dir}/page_{page_index}_to_{min(page_index + page_size, num_pages)}.pdf"
            with open(output_pdf_path, 'wb') as output_pdf:
                writer_pdf.write(output_pdf)

page_size = 5
maximum_file_size = 4.99
input_pdf_path = 'data/Operating System Concepts.pdf'
output_dir = f"dumps/Operating System Concepts Split {page_size} in {page_size} pages"

try:
    os.makedirs(output_dir)
except FileExistsError as fee:
    print("Folder already exists")
    
pdf_split(input_pdf_path=input_pdf_path, output_dir=output_dir, page_size=page_size, maximum_file_size=maximum_file_size)