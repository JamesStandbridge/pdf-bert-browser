#pdf_text_extraction_script.py

from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None

def process_pdf_directory(directory_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    original_filenames = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            text = extract_text_from_pdf(file_path)
            if text:
                text = text.lower()
                output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.txt')
                with open(output_file_path, 'w') as file:
                    file.write(text)
                original_filenames.append(filename)

    return original_filenames
