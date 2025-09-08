'''
Vector store utilities for document retrieval'''

from dotenv import load_dotenv
import os
import io
from contextlib import redirect_stderr
from chromadb import Client, Settings
from chromadb.utils import embedding_functions
from typing import Dict, List
from LangGraph_chatbot.data.data_config import NUM_CHUNKS_TO_RETRIEVE, SIMILARITY_DISTANCE_THRESHOLD

# Load environment variables
load_dotenv()

def get_project_vector_store_path(project_id: str) -> str:
    '''
    Get the vector store directory for a specific project
    '''

    if not project_id:
        raise ValueError("project_id must be provided")
    
    project_dir = os.path.join(os.getenv('UPLOAD_FOLDER'), project_id)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir

def get_project_client(project_id: str) -> Client:
    '''
    Get a ChromaDB client for a specific project
    '''

    vector_store_dir = get_project_vector_store_path(project_id)
    
    # Create a temporary stderr to capture telemetry errors
    temp_stderr = io.StringIO()
    
    try:
        with redirect_stderr(temp_stderr):
            client = Client(Settings(
                persist_directory=vector_store_dir,
                anonymized_telemetry=False,
                is_persistent=True
            ))
        return client
    except Exception as e:
        # If there's a real error, re-raise it
        raise ValueError(f"Failed to get project client: {str(e)}")

# OpenAI embeddings
embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name='text-embedding-3-small'
)

def check_collection_exists(collection_name: str, project_id: str) -> bool:
    '''
    Check if a collection exists in the vector store
    '''

    client = get_project_client(project_id)

    try:
        client.get_collection(collection_name)
        return True
    except Exception:
        return False

def create_collection_if_not_exists(collection_name: str, project_id: str) -> None:
    '''
    Create a collection in the vector store
    '''

    client = get_project_client(project_id)
    try:
        return client.create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={'hnsw:space': 'cosine'}
        )
    except Exception as e:
        raise ValueError(f"Failed to create collection {collection_name}: {str(e)}")
    
def add_document_chunks(collection_name: str, documents: List[Dict], project_id: str):
    '''
    Add documents chunks to the vector store
    '''
    client = get_project_client(project_id)

    try:
        collection = client.get_collection(collection_name)

        texts = [doc['text'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        ids = [doc['id'] for doc in documents]


        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    except Exception as e:
        raise ValueError(f"Failed to add documents to collection {collection_name}: {str(e)}")
    
def search_similar_chunks(collection_name: str, questions: List[str], project_id: str, k: int = NUM_CHUNKS_TO_RETRIEVE) -> List[Dict]:
    '''
    Search for similar chunks in the vector store
    '''

    client = get_project_client(project_id)

    try:
        collection = client.get_collection(collection_name)

        results = collection.query(
            query_texts=questions,
            n_results=k
        )

        return [
            {
                'text': doc,
                'metadata': metadata,
                'distance': dist
            }
            for doc, metadata, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0])
            if 1 - dist > SIMILARITY_DISTANCE_THRESHOLD
        ]
    except Exception as e:
        raise ValueError(f"Failed to search for similar chunks in collection {collection_name}: {str(e)}")
    