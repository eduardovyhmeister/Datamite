"""A module for managing ChromaDB in our RAG system. This provides functions
for basic management such as the creation of a DB, populating the DB with
documents, etc.
"""

import os

import chromadb
from langchain_core.documents import Document

from utils import environment

DEFAULT_COLLECTION_NAME = "datamite-RAG"
DEFAULT_DIRECTORY = environment.CHROMA_DB_FOLDER + os.sep + "chromadb"

# -----------------------------------------------------------------------------
# Knowledge base creation:

def get_vector_db(collection_name: str = DEFAULT_COLLECTION_NAME,
                  persist_directory: str = DEFAULT_DIRECTORY) -> chromadb.Collection:
    """Get the connector to the vector DB for the provided collection name.
    If the DB doesn't exist yet, creates it. Uses the default embedding model
    from ChromaDB which is `all-MiniLM-L6-v2`. The cosine distance is used to
    compare documents.
    
    Args:
        collection_name (str): A name for your collection in the vector database.
            Will be used to search the DB during retrieval.
        persist_directory (str): The directory in which the DB will be created or
            retrieved.
    
    Returns:
        chromadb.Collection - A client connected to the database's collection
        that can be used to store or search for documents.
    """
    # Get the collection:
    client = chromadb.Client(chromadb.Settings(persist_directory = persist_directory,
                                               anonymized_telemetry = False,
                                               is_persistent = True))
    return client.get_or_create_collection(name = collection_name, 
                                           metadata={'hnsw:space': 'cosine'})


def store_documents(vector_store: chromadb.Collection, documents: list[Document]):
    """Stores the provided documents in the provided collection.
    
    The only reason for this function is to make it more "Langchain-friendly".
    
    Args:
        vector_store (chromadb.Collection): The connector to use to store the
            documents. Can be obtained through `get_vector_db()`.
        documents (list[Document]): A list of langchain documents to add to
            the vector DB.
    """
    vector_store.add(ids = [doc.id for doc in documents], 
                     metadatas = [doc.metadata for doc in documents], 
                     documents = [doc.page_content for doc in documents])

# -----------------------------------------------------------------------------
# Retrieval functions:

def basic_retrieval(query:str, vector_store: chromadb.Collection, 
                    k:int = 3, threshold:float = 0.3) -> list[Document]:
    """Retrieves the documents in the vector DB that are the closest to the
    query. The algorithm used here a very basic and this may not yield great
    results.
    
    Args:
        query (str): The query from the user (e.g., a question).
        vector_store (chromadb.Collection): The chromaDB collection connector.
        k (int): The maximum number of documents to retrieve. Defaults to 3.
        threshold (float): The minimum similarity required for a document to
            be selected. Defaults to 0.3. Similarity = 1 - Cosine Distance.
            
    Returns:
        list[tuple(Document, similarity_score)] - The retrieved documents sorted
        from most relevant to least relevant. A similarity of 1 means highly relevant,
        a similarity of 0 means not relevant at all.
    """
    query_result = vector_store.query(query_texts = query, n_results = k)
    return [Document(page_content = text,
                     metadata = metadata,
                     id = id)
            for text, metadata, id, distance in zip(query_result["documents"][0], 
                                                    query_result["metadatas"][0], 
                                                    query_result["ids"][0],
                                                    query_result["distances"][0])
            if 1 - distance >= threshold]


# -----------------------------------------------------------------------------
# Test that it works:
if __name__ == "__main__":
    collection = get_vector_db()
    results = basic_retrieval("What is accessibility?", collection)
    print(f"Nb results {len(results)}")
    print(f"First document: {results[0]}")
    print("*" * 80)
    print(f"Second document: {results[1]}")
    print("*" * 80)
    print(f"Third document: {results[2]}")
    print("*" * 80)