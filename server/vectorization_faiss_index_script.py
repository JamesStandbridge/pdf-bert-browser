#vectoriztion_faiss_index_script.py

import os
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import faiss

def add_to_faiss_index(doc_vector, faiss_index):
    """
    Ajoute un nouveau vecteur document à l'index FAISS existant.
    
    Args:
    doc_vector (array): Le vecteur du nouveau document à ajouter.
    faiss_index (faiss.Index): L'index FAISS existant.
    
    """
    # Assurez-vous que le vecteur document est de type float32
    doc_vector = np.array(doc_vector).astype('float32').reshape(1, -1)

    # Ajoutez le vecteur à l'index
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
        doc_vectors.append(doc_vector)

    return (tokenizer, model), doc_vectors

def create_faiss_index(doc_vectors):
    dimension = len(doc_vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(doc_vectors).astype('float32'))
    return index