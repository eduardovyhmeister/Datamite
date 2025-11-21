"""A module providing functions used to process documents into chunks for
the creation of a knowledge base to be used in a RAG system. 

The functions provided here all take a filepath as an input and return a
list of strings corresponding to the chunks to be embedded and saved into
a vector database. For managing the vector database (creation, populating,
deleting, etc.), see module `chroma_manager`. If you want your own file
processors to be used in the same way, they should also take the filepath
as a first argument, and be added to the file registry at the bottom of
the module.

If you need more file formats to be supported, you can implement your own
functions in here.
"""

import csv
import pathlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

# Get the logger for the file processors.
from utils import environment
from utils import custom_logger as logging
logger = logging.get_logger(__name__, environment.LOGGING_LEVEL)


# -----------------------------------------------------------------------------
# File processors:

# To be used as default parameter for the CSV file reader. This enables proper
# management of quotes, escape chars, etc.
DEFAULT_CSV_PARAMS = {
    "quotechar": '"',
    "delimiter": ',',
    "quoting": csv.QUOTE_ALL,
    "skipinitialspace": True,
    "escapechar": "\\",
}

def process_csv(filepath: str, column_names: list[str] = None, **csvreader_kwargs):
    """Processes a CSV and create a document per row. Each document is organised
    as follows:
    ```
    Document type: {document_type} # The document type is determined from the name of the file.
    {column_names[0]}: {row[i][0]}
    {column_names[1]}: {row[i][1]}
    ...
    ```
    Invalid rows are skipped but logs will show errors.

    Args:
        filepath (str): The path to the file to process.
        column_names (list[str]): The name of the columns. If left empty, it assumes
            the header is the first line of the processed file. If you set this, then
            it is assumed that the file does not contain a header. The number of columns
            provided in this list should correspond to the actual number of columns
            in the file, otherwise, it will log errors.
        **csvreader_kwargs (dict[str: any]): The arguments to pass to the `csv.reader()`
            function. This way you can configure how your CSV file should be read.
    
    Returns:
        list[str] - A list of documents in the form of strings.
    """
    documents = []
    
    with open(filepath, "r") as csv_file:
        reader = csv.reader(csv_file, **csvreader_kwargs)
        document_type = pathlib.Path(filepath).stem
        
        if not column_names:
            column_names = [field_name.strip() for field_name in next(reader)]

        for line_number, row in enumerate(reader, start = 2):
            row = [column.strip() for column in row]
            
            # Check the row is compatible with the header/column_names:
            if len(row) != len(column_names):
                logger.error(f"Invalid Row Error - In file {filepath}, line {line_number} is invalid: " +
                             f"expected {len(column_names)} entries, got {len(row)} instead." +
                             f"{row}")
                continue
            
            # Build the document:
            document = ""
            document += f"Document type: {document_type}\n"
            for column, content in zip(column_names, row):
                document += f"{column}: {content}\n"
            documents.append(document)
            
    return documents            


def process_pdf(filepath: str, chunk_size: int = 500, chunk_overlap = 100):
    """Processes a PDF by extracting the text and then chunking it into small
    excerpts with a maximum size of `chunk_size` tokens.
    
    WARNING: The token splitter used here is the default one, which may count
    tokens differently from the LLM model you use.
    
    Args:
        filepath (str): The path to the file to process.
        chunk_size (int): The maximum number of tokens in a chunk.
        chunk_overlap (int): The number of tokens used as overlap between chunks.
            If set to 0, there will be no overlap between chunks. A large overlap
            keeps more context around the excerpts. Should be strictly lower than
            `chunk_size`.
    
    Returns:
        list[str] - A list of documents in the form of strings.
        
    Raises:
        ValueError if chunk_size or chunk_overlap are set to invalid values.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap should be strictly lower than chunk_size.")
    if chunk_size <= 0:
        raise ValueError("chunk_size should be strictly positive.")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap should be null or positive.")
    
    # Load the PDF as a single piece of text:
    loader = PyPDFLoader(filepath, mode = "single")
    full_text = loader.load()[0].page_content
    
    # Chunk the text based on a max number of tokens per chunk:
    text_splitter = TokenTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    chunks = text_splitter.split_text(full_text)
    return chunks


# -----------------------------------------------------------------------------
# Just register your file processors in this dictionary, they'll be used
# automatically when discovering files to be integrated in the knowledge base.
# This should be in the form "file_extension": function_name
PROCESSORS_REGISTRY = {
    ".csv": process_csv,
    ".pdf": process_pdf,
}

    
