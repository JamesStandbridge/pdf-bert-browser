from pdf_text_extraction_script import process_pdf_directory
from vectorization_faiss_index_script import load_documents, vectorize_documents, create_faiss_index
import pickle
import faiss 

def main(pdf_directory, text_directory, model_path, faiss_index_path, filenames_path):
    # Step 1: Extract text from PDFs
    process_pdf_directory(pdf_directory, text_directory)

    # Step 2: Load documents from the text directory
    documents = load_documents(text_directory)

    # Step 3: Vectorize the documents
    model, doc_vectors = vectorize_documents(documents)

    # Step 4: Create and save the FAISS index
    faiss_index = create_faiss_index(doc_vectors)
    faiss.write_index(faiss_index, faiss_index_path)

    # Save the vectorization model and filenames
    pickle.dump(model, open(model_path, "wb"))
    filenames = list(documents.keys())  # List of filenames
    pickle.dump(filenames, open(filenames_path, "wb"))

# Example Usage
pdf_directory = 'node/files'  # Directory containing PDFs
text_directory = 'node/extracted_texts'  # Directory to store extracted texts
model_path = 'node/index/doc2vec_model.pkl'  # Path to save the vectorization model
faiss_index_path = 'node/index/faiss_index.idx'  # Path to save the FAISS index
filenames_path = 'node/index/filenames.pkl'  # Path to save the filenames list

main(pdf_directory, text_directory, model_path, faiss_index_path, filenames_path)
