from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from pydantic import BaseModel
import shutil
from typing import List
import os
from fastapi.middleware.cors import CORSMiddleware

from src.files import upload_and_process_pdf
from src.search import load_model_index_and_filenames, search

import config

class SearchRequest(BaseModel):
    query: str

app = FastAPI()

# Define paths to various directories and files from configuration
index_path = config.INDEX_PATH
model_path = config.MODEL_PATH
faiss_index_path = config.FAISS_INDEX_PATH
filenames_path = config.FILENAMES_PATH
text_path = config.TEXT_PATH
files_path = config.FILES_PATH

# Configure CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file.

    Args:
    file (UploadFile): The PDF file to be uploaded.

    Returns:
    dict: A dictionary containing the filename of the uploaded file.
    """
    # Process the uploaded PDF file
    await upload_and_process_pdf(
        file, 
        upload_directory=files_path,
        text_directory=text_path,
        model_path=model_path,
        faiss_index_path=faiss_index_path,
        filenames_path=filenames_path
    )
    return {"filename": file.filename}

@app.post("/search/", response_model=List[dict])
async def perform_search(request: SearchRequest):
    """
    Endpoint to search the indexed documents.

    Args:
    request (SearchRequest): The search query.

    Returns:
    list: A list of dictionaries containing search results.
    """
    try:
        # Load model, FAISS index, and filenames
        model, faiss_index, filenames = load_model_index_and_filenames(
            model_path, faiss_index_path, filenames_path)

        # Perform the search operation
        search_results = search(request.query, model, faiss_index, 
                                filenames, text_path)

        # Format and return the search results
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

@app.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    """
    Endpoint to retrieve a specific PDF file.

    Args:
    filename (str): The name of the PDF file to retrieve.

    Returns:
    Response: A FastAPI Response object containing the PDF file.
    """
    file_path = os.path.join('node/files', filename)
    if os.path.exists(file_path):
        # Read and return the PDF file
        with open(file_path, "rb") as file:
            file_data = file.read()

        headers = {
            'Content-Disposition': 'inline; filename="{}"'.format(filename),
            'Content-Type': 'application/pdf'
        }
        return Response(content=file_data, headers=headers, 
                        media_type='application/pdf')
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/get-all-pdf/")   
async def get_all_pdf():
    """
    Endpoint to retrieve a list of all PDF files.

    Returns:
    list: A list of filenames of all PDF files.
    """
    files = []
    # Gather all PDF filenames
    for filename in os.listdir(files_path):
        if filename.endswith(".pdf"):
            files.append(filename)
    return files

@app.delete("/reset-files/")
async def reset_data():
    """
    Endpoint to reset and clear all data.

    Returns:
    dict: A dictionary with the status of the reset operation.
    """
    try:
        # Clear directories and reset data
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
