#vectoriztion_faiss_index_script.py

import os
import gensim
import numpy as np
import faiss
import pickle

def load_documents(directory_path):
    documents = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            original_filename = filename.replace('.txt', '.pdf')
            with open(os.path.join(directory_path, filename), 'r') as file:
                documents[original_filename] = file.read().lower()
    return documents

def vectorize_documents(documents):
    tagged_data = [gensim.models.doc2vec.TaggedDocument(words=_d.split(), tags=[str(i)]) for i, _d in enumerate(documents.values())]
    model = gensim.models.Doc2Vec(tagged_data, vector_size=100, window=2, min_count=1, epochs=40)
    
    doc_vectors = [model.infer_vector(doc.split()) for doc in documents.values()]
    return model, doc_vectors

def create_faiss_index(doc_vectors):
    dimension = len(doc_vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(doc_vectors).astype('float32'))
    return index