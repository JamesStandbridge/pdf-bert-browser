# config.py

NODE_PATH = './node'
INDEX_PATH = NODE_PATH + '/index'

MODEL_PATH = INDEX_PATH + '/doc2vec_model.pkl'
FAISS_INDEX_PATH = INDEX_PATH + '/faiss_index.idx'
FILENAMES_PATH = INDEX_PATH + '/filenames.pkl'
TEXT_PATH = NODE_PATH + '/extracted_texts'
FILES_PATH = NODE_PATH + '/files'

TEST_NODE_PATH = 'tests/test-node'
TEST_INDEX_PATH = TEST_NODE_PATH + '/index'

TEST_MODEL_PATH = TEST_INDEX_PATH + '/doc2vec_model.pkl'
TEST_FAISS_INDEX_PATH = TEST_INDEX_PATH + '/faiss_index.idx'
TEST_FILENAMES_PATH = TEST_INDEX_PATH + '/filenames.pkl'
TEST_TEXT_PATH = TEST_NODE_PATH + '/extracted_texts'
TEST_FILES_PATH = TEST_NODE_PATH + '/files'




# CORS Origins
ORIGINS = [
    "http://localhost:3000/*",
    "http://localhost:3000*",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost",
    "http://51.210.255.189:3000",
    "http://51.210.255.189:3000*",
    "http://51.210.255.189:3000/*",
    "http://51.210.255.189",
]
