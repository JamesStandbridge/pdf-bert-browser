# PDF Text Search Application

This application provides a comprehensive solution for uploading PDF files, extracting text content, vectorizing the text, and enabling efficient search capabilities through a FAISS index. Built with a modern Python stack including FastAPI, Transformers, and PyTorch, it is designed to be scalable and easy to use.

## Features

-  **PDF Upload**: Users can upload PDF documents which will be processed and stored for text searching. 
-  **Text Extraction**: Extracts text from PDF documents using PDFMiner. 
-  **Text Vectorization**: Converts extracted text into numerical vectors using BERT embeddings. 
- **Efficient Searching**: Implements a FAISS index to enable fast and efficient similarity search on the vectorized text. 
- **Web Interface**: Provides a user-friendly web interface to interact with the system, allowing for PDF uploads, searching, and document retrieval.

## Getting Started

### Prerequisites

- Docker 
- Docker Compose

### Installation

Clone the repository to your local machine:

```bash
$ git clone https://github.com/your-username/your-repository.git
$ cd your-repository
```

Modify line 16 of your Dockerfile.client file to adjust the API url according to your installation: on a local machine, configure on localhost, on a server, configure on the appropriate ip.
 
Use Docker Compose to build and start the services:

```bash
$ docker-compose up --build
```

The command will start the FastAPI server and the Vite.js client, and will be accessible at the following URLs:

-   FastAPI server: `http://localhost:8000`
-   Vite.js client: `http://localhost:3000`

## Usage

Navigate to `http://localhost:3000` in your web browser to access the Vite.js client, where you can upload PDFs and perform text searches.

For direct interaction with the FastAPI server for actions like uploading PDFs or searching, you can use the provided RESTful API endpoints.

### Uploading a PDF

To upload a PDF document:

```bash
$ curl -X 'POST' \
  'http://localhost:8000/upload-pdf/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path_to_pdf_file.pdf'
  ```

### Searching

To perform a search:

```bash 
curl -X 'POST' \
  'http://localhost:8000/search/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"query": "your search query"}'
  ``` 

## All API Endpoints

-   `POST /upload-pdf/`: Upload a PDF file for processing.
-   `POST /search/`: Search the indexed documents with a query.
-   `GET /get-all-pdf/`: Retrieve a list of all available PDF filenames.
-   `GET /get-pdf/{filename}`: Retrieve a specific PDF file by its filename.
-   `DELETE /reset-files/`: Reset the application data by clearing all documents and indexes.