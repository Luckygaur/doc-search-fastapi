# FastAPI Server for Retrieval-Augmented Generation (RAG)

This repository contains a streamlined FastAPI server designed for Retrieval-Augmented Generation (RAG). The server leverages ChromaDB’s persistent client to efficiently ingest and query documents in multiple formats, including PDF, DOC, DOCX, and TXT. It uses the sentence-transformers/all-MiniLM-L6-v2 model from Hugging Face for CPU-optimized sentence embeddings, while non-blocking API endpoints ensure efficient concurrency management.

## Key Features
- *Document Ingestion & Retrieval*: Supports storing and querying documents (PDF, DOC, DOCX, TXT) with ChromaDB.
- *High-Quality Embeddings*: Embeddings generated with sentence-transformers/all-MiniLM-L6-v2.
- *Efficient API Design*: FastAPI enables non-blocking, concurrent request handling.

## Technology Stack
- *FastAPI*: Framework for creating API endpoints.
- *ChromaDB*: Vector storage for managing and querying document embeddings.
- *Sentence-Transformers*: Generates document embeddings using all-MiniLM-L6-v2.
- *Python*: Core programming language.
- *Uvicorn*: ASGI server for running the FastAPI app.

## Libraries and Technologies
1. *FastAPI*: High-performance Python framework for building APIs.
2. *Uvicorn*: ASGI server optimized for running FastAPI applications.
3. *ChromaDB*: Vector database to store and retrieve embeddings.
4. *Sentence-Transformers*: Provides embedding generation with transformer models.
5. *Langchain*: Assists in processing different document types.
6. *Python Standard Libraries*: Includes uuid for ID generation and logging for monitoring.

## Getting Started
### Prerequisites
- Python 3.8+
- pip for package management

### Installation
1. *Clone the Repository*
   sh
   git clone https://github.com/<username>/fastapi-rag-server.git
   cd fastapi-rag-server
   

2. *Install Dependencies*
   sh
   pip install -r requirements.txt
   

3. *Run the Server*
   sh
   uvicorn main:app --reload
   
   The server will be available at http://127.0.0.1:8000.

## API Endpoints
### 1. /ingest/ [POST]
Uploads documents (PDF, DOC, DOCX, TXT) for retrieval.
- *Request*: Multipart form containing files to ingest.
- *Example Input*: sample1.txt, sample2.pdf
- *Example Response*:
  json
  { "status": "Documents uploaded successfully" }
  

### 2. /query/ [GET]
Searches the uploaded documents.
- *Parameters*: query_text (str) - Text to search for.
- *Example URL*: http://127.0.0.1:8000/query/?query_text=What is FastAPI?
- *Example Response*:
  json
  {
    "results": [
      {
        "filename": "sample1.txt",
        "score": 0.7214,
        "text": "Title: Introduction to FastAPI\n\nFastAPI is a modern, fast, high-performance web framework..."
      }
    ]
  }
  

### 3. /database/ [GET]
Retrieves all stored documents’ metadata and text.
- *Example Response*:
  json
  {
    "documents": [
      { "filename": "sample1.txt", "text": "Introduction to FastAPI..." },
      { "filename": "sample2.pdf", "text": "Sample PDF document text..." }
    ]
  }
  

## Running the Server
1. *Start the Server*
   sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   
   Access it at http://localhost:8000.

2. *Testing Endpoints*
   - Use tools like *Postman* or *Thunder Client* for interaction.

## Usage Example
### Document Upload
Upload documents using a POST request to /ingest/.
- *URL*: http://localhost:8000/ingest/
- *Method*: POST with files in form-data.

### Document Search
Send a GET request to /query/ with the query text.
- *URL*: http://localhost:8000/query/?query_text=<your_query>

## Contributing
Contributions are welcome! Submit a Pull Request.

For questions, reach out at [gaurlucky102003@gmail.com](mailto:gaurlucky102003@gmail.com) or visit [Luckygaur](https://github.com/Luckygaur).

## License
This project is licensed under the MIT License.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Sentence-Transformers](https://www.sbert.net/)
- [Langchain](https://langchain.com/)
