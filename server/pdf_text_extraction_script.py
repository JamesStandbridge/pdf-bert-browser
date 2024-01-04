from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file.

    Args:
        pdf_path (str): The file path to the PDF from which text is to be extracted.

    Returns:
        str: The extracted text as a string if extraction is successful, 
             or None if an error occurs.

    Raises:
        Exception: An error occurred during text extraction with the error message.
    """
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None

def process_pdf_directory(directory_path, output_directory):
    """
    Processes each PDF file in the specified directory, extracting text and saving 
    it as a .txt file.

    This function reads all PDF files in the given directory, extracts their text, 
    converts it to lowercase,
    and saves each document's text in a separate .txt file in the output directory.
    The name of the text file
    is derived from the original PDF file name.

    Args:
        directory_path (str): The directory path containing PDF files to be processed.
        output_directory (str): The directory path where extracted text files will be saved.

    Returns:
        list of str: A list of original filenames of the processed PDFs.

    Creates:
        Text files (.txt): For each PDF, a corresponding text file is created in the 
        output directory.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    original_filenames = []

    # Process each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            text = extract_text_from_pdf(file_path)
            if text:
                # Convert text to lowercase and save it
                text = text.lower()
                output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.txt')
                with open(output_file_path, 'w') as file:
                    file.write(text)
                # Keep track of the original filenames
                original_filenames.append(filename)

    return original_filenames
