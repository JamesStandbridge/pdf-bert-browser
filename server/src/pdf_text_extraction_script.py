from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.

    Args:
    pdf_path (str): The file path of the PDF from which to extract text.

    Returns:
    str: The extracted text as a string. If text extraction fails, returns None.

    Exceptions:
    Catches and prints exceptions if text extraction fails, returning None.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None

def process_pdf_directory(directory_path, output_directory):
    """
    Processes all PDF files in a given directory, extracting text and 
    saving it as .txt files.

    Args:
    directory_path (str): The path to the directory containing PDF files.
    output_directory (str): The path to the directory where extracted 
    text files should be saved.

    Returns:
    list: A list of the original filenames of the processed PDFs.

    Description:
    For each PDF file in the directory, this function extracts text, converts 
    it to lowercase,
    and saves it as a .txt file in the output directory. It keeps track of the 
    filenames of the processed PDFs.
    """
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
