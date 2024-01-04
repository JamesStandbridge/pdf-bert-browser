# tests/test_pdf_text_extraction.py
import os
import shutil
from src.pdf_text_extraction_script import extract_text_from_pdf, process_pdf_directory

# Assurez-vous d'avoir un dossier test_files avec des fichiers PDF pour les tests
TEST_FILES_DIRECTORY = 'test_files'
TEST_OUTPUT_DIRECTORY = 'test_output'

def test_extract_text_from_pdf():
    # Utilisez un PDF test réel de votre dossier test_files
    test_pdf_path = os.path.join(TEST_FILES_DIRECTORY, 'ART20203995.pdf')
    text = extract_text_from_pdf(test_pdf_path)
    assert text is not None
    assert len(text) > 0  # Assurez-vous que du texte est extrait

def test_process_pdf_directory():
    if not os.path.exists(TEST_OUTPUT_DIRECTORY):
        os.makedirs(TEST_OUTPUT_DIRECTORY)
    
    # Process the test PDFs and get the original filenames
    original_filenames = process_pdf_directory(TEST_FILES_DIRECTORY, TEST_OUTPUT_DIRECTORY)
    
    # Assert that the text files are created for each PDF
    for original_filename in original_filenames:
        base, _ = os.path.splitext(original_filename)
        text_file_path = os.path.join(TEST_OUTPUT_DIRECTORY, base + '.txt')
        assert os.path.isfile(text_file_path)
        
        # Also check that the text files are not empty
        with open(text_file_path, 'r') as f:
            text = f.read()
            assert len(text) > 0

    # Cleanup the output directory after the test
    shutil.rmtree(TEST_OUTPUT_DIRECTORY)