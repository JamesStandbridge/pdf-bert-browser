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
        tokenizer_path, 
        faiss_index_path, 
        filenames_path
    ):
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_pdf_directory(upload_directory, text_directory)

    documents = load_documents(text_directory)

    # Check if model and index exist
    if os.path.exists(model_path) and os.path.exists(faiss_index_path):
        # Load existing model, tokenizer, and index
        tokenizer = pickle.load(open(tokenizer_path, "rb"))
        model = pickle.load(open(model_path, "rb"))
        faiss_index = faiss.read_index(faiss_index_path)
        filenames = pickle.load(open(filenames_path, "rb"))

        # Vectorize using existing model and tokenizer
        tokenizer, model, doc_vector = vectorize_documents(documents, (tokenizer, model))
        add_to_faiss_index(doc_vector, faiss_index)
    else:
        # Initialize and create new model, tokenizer, and index
        tokenizer, model, doc_vectors = vectorize_documents(documents)
        faiss_index = create_faiss_index(doc_vectors)
        filenames = []

    # Update filenames list
    original_filename = file.filename.replace('.pdf', '')
    if file.filename not in filenames:
        filenames.append(file.filename)

    # Save the updated model, index, and filenames
    pickle.dump(tokenizer, open(tokenizer_path, "wb"))
    pickle.dump(model, open(model_path, "wb"))
    faiss.write_index(faiss_index, faiss_index_path)
    pickle.dump(filenames, open(filenames_path, "wb"))
