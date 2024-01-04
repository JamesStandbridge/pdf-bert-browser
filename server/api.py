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
node_path = './node'
index_path = node_path + '/index'
doc2vec_model_path = index_path + '/doc2vec_model.pkl'
faiss_index_path = index_path +  '/faiss_index.idx'
filenames_path = index_path + '/filenames.pkl'
text_path = node_path + '/extracted_texts'
files_path = node_path + '/files'

# Configure CORS for the FastAPI application

origins = [
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    await upload_and_process_pdf(
        file, 
        upload_directory=files_path,
        text_directory=text_path,
        model_path=doc2vec_model_path,
        faiss_index_path=faiss_index_path,
        filenames_path=filenames_path
    )
    return {"filename": file.filename}


@app.post("/search/", response_model=List[dict])
async def perform_search(request: SearchRequest):
    try:
        model_path = doc2vec_model_path
        faiss_index_path = faiss_index_path
        filenames_path = filenames_path
        text_directory = text_path

        model, faiss_index, filenames = load_model_index_and_filenames(model_path, faiss_index_path, filenames_path)

        search_results = search(request.query, model, faiss_index, filenames, text_directory)

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


@app.get("/get-all-pdf/")   
async def get_all_pdf():
    files = []
    for filename in os.listdir(files_path):
        if filename.endswith(".pdf"):
            files.append(filename)
    return files

@app.delete("/reset-files/")
async def reset_data():
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