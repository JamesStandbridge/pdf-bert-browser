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
        upload_directory, 
        text_directory,
        model_path, 
        tokenizer_path, 
        faiss_index_path, 
        filenames_path
    ):
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Définir le chemin du fichier et vérifier s'il existe
    file_path = os.path.join(upload_directory, file.filename)
    if os.path.exists(file_path):
        # Modifier le nom du fichier pour éviter les conflits
        timestamp = int(time.time())
        file_name, file_extension = os.path.splitext(file.filename)
        new_file_name = f"{file_name}_{timestamp}{file_extension}"
        file_path = os.path.join(upload_directory, new_file_name)
    else:
        new_file_name = file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_pdf_directory(upload_directory, text_directory)

    documents = load_documents(text_directory)

    # Vérifiez si le modèle et l'index existent
    if os.path.exists(model_path) and os.path.exists(faiss_index_path):
        # Charger le modèle, le tokenizer et l'index existants
        tokenizer = pickle.load(open(tokenizer_path, "rb"))
        model = pickle.load(open(model_path, "rb"))
        faiss_index = faiss.read_index(faiss_index_path)
        filenames = pickle.load(open(filenames_path, "rb"))

        # Vectoriser en utilisant le modèle et le tokenizer existants
        tokenizer, model, doc_vector = vectorize_documents(documents, (tokenizer, model))
        add_to_faiss_index(doc_vector, faiss_index)
    else:
        # Initialiser et créer un nouveau modèle, tokenizer et index
        tokenizer, model, doc_vectors = vectorize_documents(documents)
        faiss_index = create_faiss_index(doc_vectors)
        filenames = []

    # Mettre à jour la liste des noms de fichiers
    if new_file_name not in filenames:
        filenames.append(new_file_name)

    # Sauvegarder le tokenizer, le modèle, l'index et les noms de fichiers mis à jour
    pickle.dump(tokenizer, open(tokenizer_path, "wb"))
    pickle.dump(model, open(model_path, "wb"))
    faiss.write_index(faiss_index, faiss_index_path)
    pickle.dump(filenames, open(filenames_path, "wb"))
