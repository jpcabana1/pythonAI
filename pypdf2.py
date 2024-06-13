import os
import PyPDF2

def split_pdf(file_path, output_directory, log):     
    with open(file_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        num_pages = len(pdf_reader.pages)
        for i in range(0, num_pages, 5):
            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(i, min(i + 5, num_pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            output_path = os.path.join(output_directory, f'{os.path.splitext(os.path.basename(file_path))[0]}_part_{i//5 + 1}.pdf')
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
    print(f"Split PDF '{file_path}' into parts.")
    #log.append((file_path, MSG_FILE_SPLITTED, ((os.path.getsize(file_path))/1024)/1024))