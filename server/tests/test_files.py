# tests/test_files.py

import os
from fastapi import UploadFile
from src.files import upload_and_process_pdf
import shutil
import config
import pytest

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup before tests run
    setup_directories()
    # This will run after the tests have completed
    yield
    # Teardown after tests run
    teardown_directories()

def setup_directories():
    # Creates test directories if they don't exist
    os.makedirs(config.TEST_NODE_PATH, exist_ok=True)
    os.makedirs(config.TEST_FILES_PATH, exist_ok=True)
    os.makedirs(config.TEST_TEXT_PATH, exist_ok=True)
    os.makedirs(config.TEST_INDEX_PATH, exist_ok=True)  # Make sure to create the index directory as well

def teardown_directories():
    # Clean up test directories after tests are done
    shutil.rmtree(config.TEST_NODE_PATH, ignore_errors=True)  # Removing the parent directory should suffice

@pytest.mark.asyncio
async def test_upload_and_process_pdf():
    # Use an actual file from the test_files directory
    test_file_path = os.path.join('test_files', 'editorial.pdf')
    
    # Open the actual file in binary read mode
    with open(test_file_path, 'rb') as file:
        # Create an UploadFile object from the actual PDF
        test_file = UploadFile(filename='editorial.pdf', file=file)
        
        await upload_and_process_pdf(
            test_file,
            upload_directory=config.TEST_FILES_PATH, 
            text_directory=config.TEST_TEXT_PATH, 
            model_path=config.TEST_MODEL_PATH, 
            faiss_index_path=config.TEST_FAISS_INDEX_PATH, 
            filenames_path=config.TEST_FILENAMES_PATH
        )
    
    # The path where the uploaded file should be saved
    uploaded_file_path = os.path.join(config.TEST_FILES_PATH, 'editorial.pdf')
    
    # Check if the file was saved correctly during the upload and processing
    assert os.path.isfile(uploaded_file_path)
    
# The removal of the file is not needed here as the teardown_directories will handle it
