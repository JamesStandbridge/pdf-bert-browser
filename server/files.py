import os
import pickle
import shutil
import time
from fastapi import UploadFile
import faiss
from pdf_text_extraction_script import process_pdf_directory
from vectorization_faiss_index_script import load_documents, vectorize_documents, create_faiss_index, add_to_faiss_index

async def upload_and_process_pdf(
        file: UploadFile, 
        upload_directory: str, 
        text_directory: str,
        model_path: str, 
        tokenizer_path: str, 
        faiss_index_path: str, 
        filenames_path: str
    ):
    """
    Process an uploaded PDF file by saving it, extracting text, vectorizing the text,
    and adding the vector to a FAISS index.

    This function performs several steps:
    1. Saves the uploaded file to the specified upload directory, handling 
       name conflicts by renaming.
    2. Processes the PDF to extract text and saves the extracted text to the text directory.
    3. Loads existing model, tokenizer, and FAISS index if they exist; 
       otherwise initializes them.
    4. Vectorizes the extracted text using the (possibly new) model and tokenizer.
    5. Adds the new document vector to the FAISS index.
    6. Updates the list of filenames with the new file.
    7. Saves the updated tokenizer, model, FAISS index, and filenames list to disk.

    Args:
        file (UploadFile): The uploaded PDF file.
        upload_directory (str): Path to the directory where the PDF will be stored.
        text_directory (str): Path to the directory where extracted texts will be saved.
        model_path (str): Path to the saved model file.
        tokenizer_path (str): Path to the saved tokenizer file.
        faiss_index_path (str): Path to the saved FAISS index file.
        filenames_path (str): Path to the saved filenames list file.

    Raises:
        HTTPException: If an error occurs during the file upload and processing.
    """

    # Ensure the upload directory exists
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Define the file path and check for existence
    file_path = os.path.join(upload_directory, file.filename)
    if os.path.exists(file_path):
        # Modify the file name to avoid conflicts
        timestamp = int(time.time())
        file_name, file_extension = os.path.splitext(file.filename)
        new_file_name = f"{file_name}_{timestamp}{file_extension}"
        file_path = os.path.join(upload_directory, new_file_name)
    else:
        new_file_name = file.filename

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the PDF and save it
    process_pdf_directory(upload_directory, text_directory)

    # Load or initialize documents and vectorization artifacts
    documents = load_documents(text_directory)
    if os.path.exists(model_path) and os.path.exists(faiss_index_path):
        # Load existing tokenizer, model, and FAISS index
        tokenizer = pickle.load(open(tokenizer_path, "rb"))
        model = pickle.load(open(model_path, "rb"))
        faiss_index = faiss.read_index(faiss_index_path)
        filenames = pickle.load(open(filenames_path, "rb"))

        # Vectorize using the existing model and tokenizer
        tokenizer, model, doc_vector = vectorize_documents(documents, (tokenizer, model))
        add_to_faiss_index(doc_vector, faiss_index)
    else:
        # Initialize and create a new model, tokenizer, and index
        tokenizer, model, doc_vectors = vectorize_documents(documents)
        faiss_index = create_faiss_index(doc_vectors)
        filenames = []

    # Update filenames list
    if new_file_name not in filenames:
        filenames.append(new_file_name)

    # Save updated artifacts
    pickle.dump(tokenizer, open(tokenizer_path, "wb"))
    pickle.dump(model, open(model_path, "wb"))
    faiss.write_index(faiss_index, faiss_index_path)
    pickle.dump(filenames, open(filenames_path, "wb"))
