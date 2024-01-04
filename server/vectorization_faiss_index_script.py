import os
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import faiss

def add_to_faiss_index(doc_vector, faiss_index):
    """
    Adds a document vector to a FAISS index.

    Args:
        doc_vector (np.ndarray): The document vector to be added to the index.
        faiss_index (faiss.IndexFlatL2): The FAISS index to which the vector will be added.

    Raises:
        ValueError: If the dimension of the vector does not match the dimension 
        of the FAISS index.
    """
    # Ensure that the vector is a numpy array of type float32
    doc_vector = np.array(doc_vector).astype('float32')
    # Verify that the vector's dimension matches the FAISS index's dimension
    if doc_vector.shape[-1] != faiss_index.d:
        raise ValueError(f"Vector dimension ({doc_vector.shape[-1]}) does not match FAISS index dimension ({faiss_index.d})")
    # Reshape the vector for compatibility with the FAISS index
    doc_vector = doc_vector.reshape(-1, faiss_index.d)
    # Add the vector to the index
    faiss_index.add(doc_vector)

def load_documents(directory_path):
    """
    Loads documents from a specified directory, reading them into memory.

    Args:
        directory_path (str): The path to the directory containing the text files.

    Returns:
        dict: A dictionary where keys are original filenames and values are the 
        content of files.
    """
    documents = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            original_filename = filename.replace('.txt', '.pdf')
            with open(os.path.join(directory_path, filename), 'r') as file:
                documents[original_filename] = file.read().lower()
    return documents

def vectorize_documents(documents, model=None):
    """
    Vectorizes the documents using BERT embeddings.

    If a model is provided, it will use the given model and tokenizer for the vectorization.
    Otherwise, it will load a pre-trained 'bert-base-uncased' model and tokenizer.

    Args:
        documents (dict): A dictionary of documents with their content.
        model (tuple, optional): A tuple of (BertTokenizer, BertModel) if they 
        are already loaded. Defaults to None.

    Returns:
        tuple: A tuple containing the tokenizer, model, and list of document vectors.
        
    Raises:
        ValueError: If document vectors are of inconsistent dimensions.
    """
    expected_dimension = 768  # Standard dimension for 'bert-base-uncased'

    # Load BERT tokenizer and model if not already provided
    if model is None:
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
    else:
        tokenizer, model = model

    doc_vectors = []
    for doc in documents.values():
        # Tokenize the document in segments
        tokenized_doc = tokenizer(doc, add_special_tokens=True, truncation=True, max_length=512, return_tensors="pt")
        input_ids = tokenized_doc['input_ids']
        attention_mask = tokenized_doc['attention_mask']

        # Vectorize each segment
        segment_embeddings = []
        for ids, mask in zip(input_ids, attention_mask):
            with torch.no_grad():
                outputs = model(input_ids=ids.unsqueeze(0), attention_mask=mask.unsqueeze(0))
            segment_embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())

        # Combine segment embeddings
        doc_vector = np.mean(segment_embeddings, axis=0)
        if len(doc_vector) != expected_dimension:
            raise ValueError(f"Vector dimension ({len(doc_vector)}) is inconsistent with the expected dimension.")
        doc_vectors.append(doc_vector)

    return tokenizer, model, doc_vectors

def create_faiss_index(doc_vectors):
    """
    Creates a FAISS index for the given list of document vectors.

    Args:
        doc_vectors (list of np.ndarray): The list of document vectors to be indexed.

    Returns:
        faiss.IndexFlatL2: A FAISS index object containing the added vectors.
    
    Raises:
        ValueError: If the list of document vectors is empty or if vectors have 
                    inconsistent dimensions.
    """
    if len(doc_vectors) == 0:
        raise ValueError("Document vectors list is empty.")

    # Verify that all vectors have the same dimension
    first_vector_dimension = len(doc_vectors[0])
    if not all(len(vector) == first_vector_dimension for vector in doc_vectors):
        raise ValueError("Document vectors do not all have the same dimension.")

    dimension = first_vector_dimension
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(doc_vectors).astype('float32'))

    return index
