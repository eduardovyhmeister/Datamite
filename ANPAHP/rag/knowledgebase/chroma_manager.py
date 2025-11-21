"""A module for managing ChromaDB in our RAG system. This provides functions
for basic management such as the creation of a DB, populating the DB with
documents, etc.
"""
import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DEFAULT_COLLECTION_NAME = "datamite-RAG"

# -----------------------------------------------------------------------------
# Knowledge base creation:

def get_vector_db(collection_name: str,
                  persist_directory: str, 
                  model_name = "all-MiniLM-L6-v2") -> Chroma:
    """Get the connector to the vector DB for the provided collection name.
    If the DB doesn't exist yet, creates it.
    
    Args:
        collection_name (str): A name for your collection in the vector database.
            Will be used to search the DB during retrieval.
        persist_directory (str): The directory in which the DB will be created or
            retrieved.
        model_name (str): The name of the model to get from HuggingFace. Defaults
            to 'all-MiniLM-L6-v2'.
    """
    # Get the embedding model:
    embedding_function = HuggingFaceEmbeddings(model_name = model_name)
    
    # Get the ChromaDB manager from Langchain:
    return Chroma(
        collection_name = collection_name,
        embedding_function = embedding_function,
        persist_directory = persist_directory,
    )


# -----------------------------------------------------------------------------
# Retrieval functions:

def basic_retrieval(query:str, vector_store: Chroma, k:int = 3, threshold:float = 0.3):
    """Retrieves the documents in the vector DB that are the closest to the
    query. The algorithm used here a very basic and this may not yield great
    results.
    
    Args:
        query (str): The query from the user (e.g., a question).
        vector_store (Chroma): The chromaDB connector.
        k (int): The maximum number of documents to retrieve. Defaults to 3.
        threshold (float): The minimum similarity required for a document to
            be selected. Defaults to 0.3.
            
    Returns:
        list[tuple(Document, similarity_score)] - The retrieved documents sorted
        from most relevant to least relevant. A similarity of 1 means highly relevant,
        a similarity of 0 means not relevant at all.
    """
    return vector_store.similarity_search_with_relevance_scores(query, k, score_threshold = threshold)
