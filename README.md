# Project Title

## Description

This project is a full-stack application featuring a FastAPI backend and a SAP React Typescript frontend. The backend handles PDF uploads, processing, and allows users to perform searches on the indexed data. The frontend provides a user-friendly interface for interacting with the backend services.

## Features and Functionality

### Backend (FastAPI)

- **PDF Processing and Text Extraction**: The backend allows users to upload PDF documents. It then processes these documents, extracting text for further operations.
- **Document Indexing**: Extracted text from PDFs is indexed using efficient data structures, enabling quick and accurate search functionality.
- **Search Functionality**: Users can search through the indexed texts using keywords or phrases. The system supports both exact and approximate search methods.
- **PDF Retrieval**: The backend provides endpoints to retrieve either specific PDF documents or a list of all available PDFs.
- **Data Reset Feature**: There is an endpoint to reset the system, clearing all processed data and indices, useful for maintenance or reinitialization.

### Frontend (SAP React Typescript)

- **User Interface for PDF Upload**: The frontend offers a simple and intuitive interface for users to upload PDF documents to be processed and indexed.
- **Search Interface**: Users can easily perform searches on the indexed data. The interface provides options for keyword input and displays the search results clearly.
- **Document Access**: The frontend allows users to view and download the PDF documents directly through the interface.
- **Responsive Design**: The application is designed to be responsive and user-friendly, ensuring a smooth experience across various devices and screen sizes.

### Docker Integration

- **Containerized Application**: Both the frontend and backend are containerized using Docker, ensuring easy deployment and a consistent environment across different systems.
- **Easy Setup**: With Docker Compose, the application can be set up and run with minimal configuration, making it easy for users to get started.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setting Up the Environment

1.  **Clone the repository:**
    ```bash
     $ git clone [URL_TO_REPOSITORY]
     $ cd [REPOSITORY_NAME]
    ```
2.  **Build the Docker containers:**

    This command builds both the FastAPI server and the ViteJS client.

    ```bash
    $ docker-compose build
    ```

### Running the Application

1.  **Start the Docker containers:**

    ```bash
    $ docker-compose up
    ```

    This command starts the FastAPI server on port 8000 and the ViteJS client on port 3000.

2.  **Accessing the Application:**

    - The FastAPI backend server will be available at `http://localhost:8000`.
    - The React frontend client can be accessed at `http://localhost:3000`.

## Usage

### FastAPI Backend

- **Upload PDF:** Use the `/upload-pdf/` endpoint to upload PDF files for processing and indexing.
- **Search:** Perform searches on the indexed data using the `/search/` endpoint.
- **Retrieve PDFs:** Access individual or all PDF files via `/get-pdf/{filename}` and `/get-all-pdf/` endpoints, respectively.
- **Reset Data:** Clear all data using the `/reset-files/` endpoint.

### React Frontend

Interact with the frontend application through your web browser to upload PDFs and perform searches. The interface communicates with the FastAPI backend to provide a seamless user experience.

## Development

For development purposes, you can make changes to the FastAPI backend or the React frontend. The changes will be reflected upon rebuilding the Docker containers.
