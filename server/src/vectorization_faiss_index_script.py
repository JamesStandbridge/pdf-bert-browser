import os
import gensim
import numpy as np
import faiss
from sklearn.decomposition import PCA


def load_documents(directory_path):
    """
    Loads documents from a specified directory and stores their contents in a dictionary.

    Args:
    directory_path (str): The path to the directory containing text files.

    Returns:
    dict: A dictionary where keys are the original filenames (converted from .txt to .pdf) and 
          values are the contents of the files.

    Description:
    Reads all text files in the given directory, converts their content to lowercase, and 
    stores them in a dictionary with their corresponding original PDF filenames.
    """
    documents = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            original_filename = filename.replace('.txt', '.pdf')
            with open(os.path.join(directory_path, filename), 'r') as file:
                documents[original_filename] = file.read().lower()
    return documents

def vectorize_documents(documents, vector_size=300, window=10, min_count=2, epochs=40, n_components=1):
    """
    Vectorizes documents using the Doc2Vec model with adjustable parameters.

    Args:
    documents (dict): A dictionary of documents.
    vector_size (int): The dimensionality of the feature vectors.
    window (int): The maximum distance between the current and predicted word.
    min_count (int): Ignores all words with total frequency lower than this.
    epochs (int): Number of iterations over the corpus.

    Returns:
    tuple: A trained Doc2Vec model and a list of document vectors.
    """

    tagged_data = [gensim.models.doc2vec.TaggedDocument(words=_d.split(), tags=[str(i)]) for i, _d in enumerate(documents.values())]
    model = gensim.models.Doc2Vec(tagged_data, vector_size=vector_size, window=window, min_count=min_count, epochs=epochs)

    
    # Inferring and normalizing document vectors
    doc_vectors = [model.infer_vector(doc.split()) for doc in documents.values()]
    # Normalize each vector to have unit length
    doc_vectors = [vec / np.linalg.norm(vec) if np.linalg.norm(vec) != 0 else np.zeros_like(vec) for vec in doc_vectors]

    # Réduction de dimension avec PCA
    # pca = PCA(n_components=n_components)
    # doc_vectors = pca.fit_transform(doc_vectors)

    return model, doc_vectors

def create_faiss_index(doc_vectors):
    """
    Creates a FAISS index for the given document vectors using 
    IndexFlatIP for cosine similarity.

    Args:
    doc_vectors (list): A list of normalized document vectors.

    Returns:
    faiss.IndexFlatIP: A FAISS index object for the document vectors 
    based on cosine similarity.
    """
    dimension = len(doc_vectors[0])
    # Using IndexFlatIP for cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(np.array(doc_vectors).astype('float32'))
    return index
