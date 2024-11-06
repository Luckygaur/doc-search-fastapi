from fastapi import FastAPI, UploadFile, File
import uvicorn
from chromadb import Client as ChromaService
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from typing import List
import logging
import uuid

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
log_handler = logging.getLogger(_name_)

# Load SentenceTransformer model (CPU)
try:
    transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    log_handler.info("SentenceTransformer model loaded successfully.")
except Exception as load_error:
    log_handler.error(f"Model loading failed: {str(load_error)}")
    raise load_error

# Configure ChromaDB client for persistence
try:
    chroma_service = ChromaService()
    doc_repo = chroma_service.get_or_create_collection(name="file_docs")
    log_handler.info("ChromaDB client initialized; collection created.")
except Exception as db_error:
    log_handler.error(f"ChromaDB initialization error: {str(db_error)}")
    raise db_error

@app.post("/ingest/", response_class=JSONResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """ Endpoint to upload documents for later search """
    file_entries = []
    vector_data = []
    file_ids = []
    
    try:
        # Read files and prepare for ingestion
        for file in files:
            try:
                file_content = await file.read()
                file_text = file_content.decode('utf-8')
                file_id = str(uuid.uuid4())
                doc_info = {"text": file_text, "metadata": {'filename': file.filename}}
                file_entries.append(doc_info)
                file_ids.append(file_id)
                log_handler.info(f"File '{file.filename}' read successfully.")

            except UnicodeDecodeError:
                log_handler.error(f"Cannot decode '{file.filename}'. Unsupported text format.")
                return JSONResponse(content={"error": f"Cannot decode '{file.filename}'."}, status_code=400)
            except Exception as file_error:
                log_handler.error(f"File reading error for '{file.filename}': {str(file_error)}")
                return JSONResponse(content={"error": f"File error: {str(file_error)}"}, status_code=500)

        # Generate embeddings for documents
        try:
            vector_data = [transformer.encode(entry["text"]).tolist() for entry in file_entries]
            log_handler.info("Document embeddings created.")
        except Exception as embedding_error:
            log_handler.error(f"Embedding generation error: {str(embedding_error)}")
            return JSONResponse(content={"error": f"Embedding error: {str(embedding_error)}"}, status_code=500)

        # Store documents in ChromaDB
        try:
            doc_repo.add(ids=file_ids, documents=[entry["text"] for entry in file_entries], 
                         metadatas=[entry["metadata"] for entry in file_entries], embeddings=vector_data)
            log_handler.info("Documents stored in ChromaDB.")
        except Exception as store_error:
            log_handler.error(f"Error adding to database: {str(store_error)}")
            return JSONResponse(content={"error": f"Database error: {str(store_error)}"}, status_code=500)

        return JSONResponse(content={"status": "Documents uploaded successfully"})

    except Exception as upload_error:
        log_handler.error(f"Unexpected error during upload: {str(upload_error)}")
        return JSONResponse(content={"error": f"Server Error: {str(upload_error)}"}, status_code=500)

@app.get("/query/", response_class=JSONResponse)
async def search_files(search_text: str):
    """ Endpoint to search documents """
    try:
        # Generate embedding for the query
        search_vector = transformer.encode(search_text).tolist()
        log_handler.info("Query embedding generated.")
        
        # Query ChromaDB
        search_results = doc_repo.query(query_embeddings=[search_vector], n_results=5)
        results_data = [
            {
                "filename": meta_info.get('filename', 'unknown') if isinstance(meta_info, dict) else 'unknown',
                "score": match_score,
                "text": doc_text
            }
            for meta_info, match_score, doc_text in zip(search_results['metadatas'], search_results['distances'], search_results['documents'])
        ]
        log_handler.info("Query processed successfully.")
        return JSONResponse(content={"results": results_data})
    
    except Exception as search_error:
        log_handler.error(f"Query error: {str(search_error)}")
        return JSONResponse(content={"error": f"Server Error: {str(search_error)}"}, status_code=500)

@app.get("/database/", response_class=JSONResponse)
async def view_all_docs():
    """ Endpoint to view all documents in the database """
    try:
        stored_docs = doc_repo.get()
        response_data = [
            {
                "filename": doc_info.get('filename', 'unknown') if isinstance(doc_info, dict) else 'unknown',
                "text": doc_text
            }
            for doc_info, doc_text in zip(stored_docs['metadatas'], stored_docs['documents'])
        ]
        log_handler.info("Database retrieval successful.")
        return JSONResponse(content={"documents": response_data})
    except Exception as db_error:
        log_handler.error(f"Database retrieval error: {str(db_error)}")
        return JSONResponse(content={"error": f"Server Error: {str(db_error)}"}, status_code=500)

if _name_ == "_main_":
    # Start the FastAPI app with live-reload enabled
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
