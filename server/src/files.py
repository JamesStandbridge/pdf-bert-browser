import os
import pickle
import shutil
from fastapi import UploadFile
import faiss

from src.pdf_text_extraction_script import process_pdf_directory
from src.vectorization_faiss_index_script import load_documents, vectorize_documents, create_faiss_index

async def upload_and_process_pdf(file: UploadFile, upload_directory, text_directory,
                                 model_path, faiss_index_path, filenames_path):
    """
    Uploads a PDF file, processes it, and updates the model and FAISS index.

    Args:
    file (UploadFile): The PDF file to be uploaded and processed.
    upload_directory (str): The directory where the uploaded files are stored.
    text_directory (str): The directory where text extracted from PDFs is stored.
    model_path (str): The path where the Doc2Vec model is saved.
    faiss_index_path (str): The path where the FAISS index is saved.
    filenames_path (str): The path where the filenames of processed documents are saved.

    Description:
    This function handles the uploading of a PDF file, extracts text from it, 
    vectorizes the text, updates the model and the FAISS index, and saves these updates.
    """
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Save the uploaded file to the upload directory
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the PDF to extract text and save it in the text directory
    original_filenames = process_pdf_directory(upload_directory, text_directory)

    # Load documents, vectorize them, and create a FAISS index
    documents = load_documents(text_directory)
    model, doc_vectors = vectorize_documents(documents)
    faiss_index = create_faiss_index(doc_vectors)

    # Save the model, FAISS index, and filenames
    pickle.dump(model, open(model_path, "wb"))
    faiss.write_index(faiss_index, faiss_index_path)
    pickle.dump(original_filenames, open(filenames_path, "wb"))
