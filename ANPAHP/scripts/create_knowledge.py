"""A module used to discover knowledge into particular folders and then
call the right file processors to process them and store them into a vector
database (we use ChromaDB).
"""

import os
import os.path
import pathlib
import shutil
import uuid

import chromadb
from langchain_core.documents import Document

from ..rag.knowledgebase import file_processors, chroma_manager

# Get the logger for the creation of the knowledge base.
from utils import environment
from utils import custom_logger as logging
logger = logging.get_logger(__name__, environment.LOGGING_LEVEL)


# -----------------------------------------------------------------------------
# Main function to create the knowledge base:

def create_knowledge_base(delete_db = True) -> chromadb.Collection:
    """Creates the knowledge base by discovering documents, processing it, and storing
    the text excerpts into a vector DB.
    
    Args:
        delete_db (bool): If set to `True`, will delete the vector DB in the DB folder
            before adding documents (use this to prevent storing multiple times the
            same documents if you restart the knowledge base creation). Defaults to
            `True`.
            
    Returns:
        chromadb.Collection - The vector store collection containing all the discovered 
        knowledge.
    """
    logger.info("Creating the knowledge base.")
    
    # Discover all the files that need to be processed:
    logger.info("Retrieving files to be processed.")
    knowledge_file_types = environment.KNOWLEDGE_FILE_TYPES
    if not knowledge_file_types:
        knowledge_file_types = list(file_processors.PROCESSORS_REGISTRY.keys())
        
    files_to_process = []
    for folder in environment.KNOWLEDGE_FOLDERS:
        try:
            files_to_process.extend(discover_documents(folder, knowledge_file_types, environment.KNOWLEDGE_SEARCH_RECURSIVELY))
        except ValueError:
            logger.warning(f"Directory '{folder}' does not exist.")
            
    if not files_to_process:
        logger.error("No file could be found to create the knowledge base." 
                     "Please check the provided knowledge folders and the file extensions specified.")
        return
        
    # Process the files found:
    csv_kwargs = file_processors.DEFAULT_CSV_PARAMS
    pdf_kwargs = {"chunk_size": environment.CHUNK_SIZE, "chunk_overlap": environment.CHUNK_OVERLAP}
    
    logger.info("Processing documents.")
    docs = process_documents(files_to_process, csv_kwargs = csv_kwargs, pdf_kwargs = pdf_kwargs)
    
    if not docs:
        logger.error("None of the found files could be processed."
                     "Please check the provided knowledge folders and the file extensions specified.")
        return
    
    # Deleting the old knowledge base if required:
    chroma_db_folder = environment.CHROMA_DB_FOLDER + os.path.sep + "chromadb"
    if delete_db:
        logger.info("Deleting the previous knowledge base.")
        try:
            shutil.rmtree(chroma_db_folder)
        except FileNotFoundError: pass
    
    logger.info("Creating/retrieving the vector DB.")
    vector_store = chroma_manager.get_vector_db()
    
    logger.info("Storing documents.")
    chroma_manager.store_documents(vector_store, docs)
    
    logger.info(f"Knowledge base created in {chroma_db_folder}.")
    return vector_store
    
    
# -----------------------------------------------------------------------------
# Utility functions:

def discover_documents(dir_path: str, extensions: list[str] = None, recursive: bool = False) -> list[str]:
    """Discovers all the documents to be processed in the provided folder.
    
    Args:
        dir_path (str): The path to the directory/folder to look into.
        extensions (list[str]): A list of extensions to look for. If specified,
            any file with an extension not in the list will be ignored. If set
            to `None`, all files will be considered.
        
    Returns:
        list[str] - A list of paths to the files to process.
        
    Raises:
        ValueError if the provided path is invalid (does not exist OR not a dir).
    """
    if not os.path.exists(dir_path):
        raise ValueError(f"Path '{dir_path}' does not exist.")
    if not os.path.isdir(dir_path):
        raise ValueError(f"Path '{dir_path}' is not a folder/directory.")
    
    # Look for files either recursively or just in the provider folder:
    files = []
    if recursive:
        for dirpath, _, filenames in os.walk(dir_path):
            files.extend([os.path.join(dirpath, f) for f in filenames])
    else:
        files = [os.path.join(dir_path, f) 
                 for f in os.listdir(dir_path) 
                 if os.path.isfile(os.path.join(dir_path, f))]
        
    # Filter by extensions:
    if extensions:
        files = [file for file in files if pathlib.Path(file).suffix in extensions]
        
    return files


def process_documents(file_paths: list[str], **kwargs) -> list[Document]:
    """Processes documents based on their extension and will extract documents
    ready to be stored into a vector database. Assumes that the provided paths
    exist. Each document will be provided a UUID. The only metadata collected
    for each document is the source of the text excerpt is coming from, here
    being the name of the file.
    
    Args:
        file_paths (list[str]): A list of paths to the files that need to be
            processed.
    
    Kwargs:
        *_kwargs (dict[str: Any]): Parameters to pass to the * file processor.
            For instance, for CSV files, this should be called `csv_kwargs`, and
            refer to the arguments of `file_processors.process_csv()`.

    Returns:
        list[str] - A list of text documents ready to be stored into a vector
        database.
    """
    processors = file_processors.PROCESSORS_REGISTRY
    documents = []
    for file in file_paths:
        path = pathlib.Path(file)
        if path.suffix not in processors:
            logger.warning(f"Could not process '{path}' because '{path.suffix}' files are not supported yet.")
            continue
        
        specific_kwargs = f"{path.suffix[1:]}_kwargs"
        try:
            if specific_kwargs not in kwargs:
                raw_docs = processors[path.suffix](file)
            else:
                raw_docs = processors[path.suffix](file, **kwargs[specific_kwargs])
        except:
            logger.exception(f"File '{file}' could not be processed.")
            continue
        
        # Create a LangChain document with a random ID:
        documents.extend([Document(page_content = text,
                                   metadata = {"source": path.name},
                                   id = str(uuid.uuid4()))
                          for text in raw_docs])
    return documents


def run():
    """Function called by the 'python manage.py runscript' command."""
    create_knowledge_base()
    

    