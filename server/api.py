#api.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from pydantic import BaseModel
import shutil

from typing import List
import os

from fastapi.middleware.cors import CORSMiddleware
from files import upload_and_process_pdf

from search import load_model_index_and_filenames, search

class SearchRequest(BaseModel):
    query: str

app = FastAPI()

# Define the paths to various directories and files
node_path = '/app/node'
index_path = node_path + '/index'
model_path = index_path + '/bert_model.pkl'
tokenizer_path = index_path + '/tokenizer.pkl'
faiss_index_path = index_path +  '/faiss_index.idx'
filenames_path = index_path + '/filenames.pkl'
text_path = node_path + '/extracted_texts'
files_path = node_path + '/files'

# Configure CORS for the FastAPI application

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://51.210.255.189:3000",
    "http://51.210.255.189",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file to the server and process it for text extraction and indexing.

    Args:
        file (UploadFile): A PDF file uploaded by the client.

    Returns:
        dict: A dictionary containing the filename of the uploaded file.
    """
    await upload_and_process_pdf(
        file, 
        upload_directory=files_path,
        text_directory=text_path,
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        faiss_index_path=faiss_index_path,
        filenames_path=filenames_path
    )
    return {"filename": file.filename}

@app.post("/search/", response_model=List[dict])
async def perform_search(request: SearchRequest):
    """
    Perform a search on the indexed documents using the provided query.

    Args:
        request (SearchRequest): The search request containing the query.

    Returns:
        List[dict]: A list of dictionaries containing search results with document info.
    """
    try:
        tokenizer, model, faiss_index, filenames = load_model_index_and_filenames(model_path, tokenizer_path, faiss_index_path, filenames_path)

        search_results = search(request.query, tokenizer, model, faiss_index, filenames, text_path)

        response = []
        for filename, distance, snippet, occurrences in search_results:
            result = {
                "document": filename,
                "distance": float(distance),
                "occurrences": occurrences,
                "snippet": snippet
            }
            response.append(result)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-all-pdf/")   
async def get_all_pdf():
    """
    Retrieve a list of all PDF filenames available on the server.

    Returns:
        List[str]: A list of PDF filenames.
    """
    files = []
    for filename in os.listdir(files_path):
        if filename.endswith(".pdf"):
            files.append(filename)
    return files

@app.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    """
    Retrieve a specific PDF file by its filename.

    Args:
        filename (str): The filename of the PDF to retrieve.

    Returns:
        Response: A FastAPI Response object containing the PDF file data.
    """
    file_path = os.path.join('node/files', filename)
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        
        headers = {
            'Content-Disposition': 'inline; filename="{}"'.format(filename),
            'Content-Type': 'application/pdf'
        }
        return Response(content=file_data, headers=headers, media_type='application/pdf')
    else:
        raise HTTPException(status_code=404, detail="File not found")
    
@app.delete("/reset-files/")
async def reset_data():
    """
    Reset the application data by clearing the contents of the text, files,
    and index directories.

    This operation deletes all the PDF files, extracted text files, and index files, 
    effectively
    resetting the application state. This is a destructive operation and should be 
    used with caution.

    Returns:
        dict: A status message indicating the outcome of the reset operation.

    Raises:
        HTTPException: An error 500 if the reset operation fails.
    """
    try:
        if os.path.exists(text_path):
            shutil.rmtree(text_path)
            os.makedirs(text_path)  
        if os.path.exists(files_path):
            shutil.rmtree(files_path)
            os.makedirs(files_path)
        if os.path.exists(index_path):
            shutil.rmtree(index_path)
            os.makedirs(index_path)

        return {"status": "success", "message": "Data has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))