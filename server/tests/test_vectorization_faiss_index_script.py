# tests/test_vectorization_faiss_index.py

import os
import numpy as np
import shutil
import config
from src.vectorization_faiss_index_script import load_documents, vectorize_documents, create_faiss_index
import pytest


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup before tests run
    setup_directories()
    # This will run after the tests have completed
    yield
    # Teardown after tests run
    teardown_directories()

def setup_directories():
    # Creates test directories if they don't exist
    os.makedirs(config.TEST_NODE_PATH, exist_ok=True)
    os.makedirs(config.TEST_FILES_PATH, exist_ok=True)
    os.makedirs(config.TEST_TEXT_PATH, exist_ok=True)
    os.makedirs(config.TEST_INDEX_PATH, exist_ok=True)  
    shutil.copy('test_files/editorial.txt', config.TEST_TEXT_PATH)


def teardown_directories():
    # Clean up test directories after tests are done
    shutil.rmtree(config.TEST_NODE_PATH, ignore_errors=True)

def test_load_documents():
    # Ensure the TEST_TEXT_PATH directory contains the 'editorial.pdf' file for testing
    documents = load_documents(config.TEST_TEXT_PATH)
    assert isinstance(documents, dict), "Expected documents to be a dictionary"
    assert 'editorial.pdf' in documents, "The 'editorial.txt' file was not loaded"
    assert len(documents['editorial.pdf']) > 0, "The document should have content"

def test_vectorize_documents():
    # Use actual documents for testing
    documents = load_documents(config.TEST_TEXT_PATH)
    model, doc_vectors = vectorize_documents(documents)
    assert model is not None, "Expected a Doc2Vec model to be created"
    assert len(doc_vectors) > 0, "Expected document vectors to be created"
    assert isinstance(doc_vectors[0], np.ndarray), "Document vectors should be numpy arrays"

def test_create_faiss_index():
    # Create some dummy vectors for testing
    doc_vectors = [np.random.rand(100).astype('float32') for _ in range(10)]
    index = create_faiss_index(doc_vectors)
    assert index is not None, "Expected a FAISS index to be created"
    assert index.ntotal == 10, "FAISS index should contain the correct number of vectors"