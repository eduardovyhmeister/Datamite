'''
This module includes utilities for loading documents into the vector store
'''
from pdfminer.high_level import extract_text
from LangGraphChatLogic.data.data_config import CHUNK_SIZE, CHUNK_OVERLAP
from typing import List
from LangGraphChatLogic.data.vector_store import check_collection_exists, create_collection_if_not_exists, add_document_chunks
import os

def extract_text_from_pdf(file_path: str) -> str:
    '''
    Extracts text from a PDF file
    '''
    return extract_text(file_path)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    '''
    Split test into overlapping chunks.
    '''
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def load_project_documents(project_id: str, files_to_process: List[str] = None, collection_name: str = None) -> list[str]:
    '''
    Loads documents for a project into a vector store.
    '''

    if not check_collection_exists(collection_name, project_id):
        create_collection_if_not_exists(collection_name, project_id)
        print(f"Collection created for project {project_id}")
    
    if not files_to_process:
        print("No files to process")
        return
    

    documents = []

    for file_path in files_to_process:
        text = None
        metadata_type = None

        try:
            if file_path.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
                text = text.replace('-\n', '')
                text = text.replace('\n', ' ')
                metadata_type = 'pdf'

            if text:
                chunks = chunk_text(text)

                for i, chunk in enumerate(chunks):
                    metadata = {
                    'file_name': os.path.basename(file_path),
                    'type': str(metadata_type),
                    'chunk': str(i),
                    'source': str(file_path)
                    }

                    documents.append({
                        'text': str(chunk),
                        'metadata': metadata, 
                        'id': f"{os.path.basename(file_path)}_{i}"
                    })
                    
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            continue
            
    if not documents:
        return
    
    try:
        add_document_chunks(collection_name=collection_name, documents=documents, project_id=project_id)
        print(f"Documents loaded for project {project_id}")
    except Exception as e:
        raise ValueError(f"Failed to add documents to vector store: {str(e)}")