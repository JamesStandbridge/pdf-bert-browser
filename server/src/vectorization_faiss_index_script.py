import os
import gensim
import numpy as np
import faiss

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

def vectorize_documents(documents):
    """
    Vectorizes documents using the Doc2Vec model.

    Args:
    documents (dict): A dictionary of documents where keys are filenames and 
    values are the document contents.

    Returns:
    tuple: A tuple containing the trained Doc2Vec model and a list of document vectors.

    Description:
    Converts the documents into a format suitable for Doc2Vec, trains the model, 
    and then infers 
    vectors for each document. These vectors can be used for similarity comparisons.
    """
    tagged_data = [gensim.models.doc2vec.TaggedDocument(words=_d.split(), tags=[str(i)]) for i, _d in enumerate(documents.values())]
    model = gensim.models.Doc2Vec(tagged_data, vector_size=100, window=2, min_count=1, epochs=40)
    
    doc_vectors = [model.infer_vector(doc.split()) for doc in documents.values()]
    return model, doc_vectors

def create_faiss_index(doc_vectors):
    """
    Creates a FAISS index for the given document vectors.

    Args:
    doc_vectors (list): A list of document vectors.

    Returns:
    faiss.IndexFlatL2: A FAISS index object for the document vectors.

    Description:
    Initializes a FAISS index with the same dimension as the document vectors 
    and adds the vectors
    to the index for efficient similarity search.
    """
    dimension = len(doc_vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(doc_vectors).astype('float32'))
    return index
