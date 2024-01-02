# files.py

import os
import pickle
import shutil
from fastapi import UploadFile
import faiss
from pdf_text_extraction_script import process_pdf_directory
from vectorization_faiss_index_script import load_documents, vectorize_documents, create_faiss_index, add_to_faiss_index

async def upload_and_process_pdf(
        file: UploadFile, 
        upload_directory, 
        text_directory,
        model_path, 
        faiss_index_path, 
        filenames_path
    ):
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_pdf_directory(upload_directory, text_directory)

    # Check if model and index exist
    if os.path.exists(model_path) and os.path.exists(faiss_index_path):
        model = pickle.load(open(model_path, "rb"))
        faiss_index = faiss.read_index(faiss_index_path)
        filenames = pickle.load(open(filenames_path, "rb"))
    else:
        model = None
        faiss_index = None
        filenames = []

    documents = load_documents(text_directory)

    # Update or create model and index
    if model is not None and faiss_index is not None:
        model, doc_vector = vectorize_documents(documents, model)
        add_to_faiss_index(doc_vector, faiss_index)
    else:
        model, doc_vectors = vectorize_documents(documents)
        faiss_index = create_faiss_index(doc_vectors)

    # Update filenames list
    original_filename = file.filename.replace('.pdf', '')
    if original_filename not in filenames:
        filenames.append(original_filename)

    # Save the updated model, index, and filenames
    pickle.dump(model, open(model_path, "wb"))
    faiss.write_index(faiss_index, faiss_index_path)
    pickle.dump(filenames, open(filenames_path, "wb"))