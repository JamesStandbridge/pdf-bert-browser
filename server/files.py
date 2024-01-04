#files.py

import os
from pdf_text_extraction_script import process_pdf_directory
from vectorization_faiss_index_script import load_documents, vectorize_documents, create_faiss_index
import pickle
import shutil
from fastapi import UploadFile
import faiss

async def upload_and_process_pdf(file: UploadFile, upload_directory, text_directory, model_path, faiss_index_path, filenames_path):
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    original_filenames = process_pdf_directory(upload_directory, text_directory)

    documents = load_documents(text_directory)
    model, doc_vectors = vectorize_documents(documents)

    faiss_index = create_faiss_index(doc_vectors)

    pickle.dump(model, open(model_path, "wb"))
    faiss.write_index(faiss_index, faiss_index_path)
    pickle.dump(original_filenames, open(filenames_path, "wb"))
