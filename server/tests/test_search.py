# tests/test_search.py

import os
import shutil
import config
from src.search import load_model_index_and_filenames, search
import pytest
import pickle
import faiss
import numpy as np

# Create a mock vector and index for testing purposes
mock_vector = np.random.rand(100).astype('float32')
mock_index = faiss.IndexFlatL2(100)
mock_index.add(np.array([mock_vector]))

# Create a mock model that returns the mock vector for any input
class MockModel:
    def infer_vector(self, words):
        return mock_vector

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup before tests run
    setup_directories()
    # This will run after the tests have completed
    yield
    # Teardown after tests run
    teardown_directories()

def setup_directories():
    os.makedirs(config.TEST_NODE_PATH, exist_ok=True)
    os.makedirs(config.TEST_FILES_PATH, exist_ok=True)
    os.makedirs(config.TEST_TEXT_PATH, exist_ok=True)
    os.makedirs(config.TEST_INDEX_PATH, exist_ok=True)  
    shutil.copy('test_files/editorial.txt', config.TEST_TEXT_PATH)

    # Save a mock model and index to the test index path
    pickle.dump(MockModel(), open(config.TEST_MODEL_PATH, 'wb'))
    faiss.write_index(mock_index, config.TEST_FAISS_INDEX_PATH)
    # Create a mock filenames list and save it
    pickle.dump(['editorial.pdf'], open(config.TEST_FILENAMES_PATH, 'wb'))

def teardown_directories():
    shutil.rmtree(config.TEST_INDEX_PATH, ignore_errors=True)

def test_load_model_index_and_filenames():
    model, index, filenames = load_model_index_and_filenames(
        config.TEST_MODEL_PATH,
        config.TEST_FAISS_INDEX_PATH,
        config.TEST_FILENAMES_PATH
    )
    assert isinstance(model, MockModel), "Expected to load a MockModel"
    
    # Testez la présence d'un attribut typique de l'index FAISS
    assert hasattr(index, 'ntotal'), "Expected the index to have 'ntotal' attribute"
    
    assert isinstance(filenames, list), "Expected to load a list of filenames"
    assert len(filenames) > 0, "Expected the filenames list to contain elements"


def test_search():
    query = "test query"
    # Load mock model, index, and filenames
    model, index, filenames = load_model_index_and_filenames(
        config.TEST_MODEL_PATH,
        config.TEST_FAISS_INDEX_PATH,
        config.TEST_FILENAMES_PATH
    )
    # Perform a search
    results = search(query, model, index, filenames, config.TEST_TEXT_PATH)
    assert isinstance(results, list), "Expected search results to be a list"
    assert len(results) > 0, "Expected at least one result from search"
    # We expect the mock model to find the query vector identical to the mock vector, so distance should be 0
    assert results[0][1] == 0, "Expected distance to be 0 for the mock search"

# Run tests with pytest from the command line
