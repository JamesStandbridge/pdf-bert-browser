#api.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from pydantic import BaseModel
from typing import List
import os

from fastapi.middleware.cors import CORSMiddleware
from files import upload_and_process_pdf

from search import load_model_index_and_filenames, search

class SearchRequest(BaseModel):
    query: str

app = FastAPI()


model_path = 'node/index/bert_model.pkl'
tokenizer_path = 'node/index/tokenizer.pkl'
faiss_index_path = 'node/index/faiss_index.idx'
filenames_path = 'node/index/filenames.pkl'
text_path = 'node/extracted_texts'
files_path = 'node/files'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    print(file)
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
    try:
        tokenizer, model, faiss_index, filenames = load_model_index_and_filenames(model_path, tokenizer_path, faiss_index_path, filenames_path)

        search_results = search(request.query, tokenizer, model, faiss_index, filenames, text_path)

        response = []

        for filename, distance, snippet, occurrences in search_results:
            result = {
                "document": filename,
                "distance": float(distance),
                "occurrences": float(occurrences),
                "snippet": snippet
            }
            response.append(result)

        print(response)

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