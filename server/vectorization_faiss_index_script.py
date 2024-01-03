#vectoriztion_faiss_index_script.py

import os
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import faiss

def add_to_faiss_index(doc_vector, faiss_index):
    # S'assurer que le vecteur est un array numpy de type float32
    doc_vector = np.array(doc_vector).astype('float32')

    # Vérifier que la dimension du vecteur correspond à la dimension de l'index FAISS
    if doc_vector.shape[-1] != faiss_index.d:
        raise ValueError(f"Dimension du vecteur ({doc_vector.shape[-1]}) ne correspond pas à celle de l'index FAISS ({faiss_index.d})")

    # Reshape le vecteur pour qu'il soit compatible avec l'index FAISS
    doc_vector = doc_vector.reshape(-1, faiss_index.d)

    # Ajouter le vecteur à l'index
    faiss_index.add(doc_vector)




def load_documents(directory_path):
    documents = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            original_filename = filename.replace('.txt', '.pdf')
            with open(os.path.join(directory_path, filename), 'r') as file:
                documents[original_filename] = file.read().lower()
    return documents


def vectorize_documents(documents, model=None):
    expected_dimension = 768  # Dimension standard pour 'bert-base-uncased'

    # Charger le tokenizer et le modèle BERT s'ils ne sont pas déjà chargés
    if model is None:
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
    else:
        tokenizer, model = model

    doc_vectors = []
    for doc in documents.values():
        # Découper le document en segments
        tokenized_doc = tokenizer(doc, add_special_tokens=True, truncation=True, max_length=512, return_tensors="pt")
        input_ids = tokenized_doc['input_ids']
        attention_mask = tokenized_doc['attention_mask']

        # Vectoriser chaque segment
        segment_embeddings = []
        for ids, mask in zip(input_ids, attention_mask):
            with torch.no_grad():
                outputs = model(input_ids=ids.unsqueeze(0), attention_mask=mask.unsqueeze(0))
            segment_embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())

        # Combiner les embeddings des segments
        doc_vector = np.mean(segment_embeddings, axis=0)
        if len(doc_vector) != expected_dimension:  # Remplacer 'expected_dimension' par la dimension attendue
            raise ValueError(f"Dimension du vecteur ({len(doc_vector)}) est incohérente avec la dimension attendue.")
        doc_vectors.append(doc_vector)

    return tokenizer, model, doc_vectors

def create_faiss_index(doc_vectors):
    if len(doc_vectors) == 0:
        raise ValueError("La liste des vecteurs document est vide.")

    # Vérifier que tous les vecteurs ont la même dimension
    first_vector_dimension = len(doc_vectors[0])
    if not all(len(vector) == first_vector_dimension for vector in doc_vectors):
        raise ValueError("Tous les vecteurs document ne sont pas de la même dimension.")

    dimension = first_vector_dimension
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(doc_vectors).astype('float32'))
    return index
