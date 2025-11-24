"""A module providing a basic RAG logic,
"""

from langchain.llms.base import LLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

from ..knowledgebase import chroma_manager
from utils import environment

# -----------------------------------------------------------------------------
# Prompt templates:

BASIC_RAG = ChatPromptTemplate(
    [
        ("system",
        "You are a helpful assistant that writes clear and professional "
        "explanations based on summaries and retrieved content from relevant files."
        ),
        ("user", "{question}"),
        ("system",
        "The following retrieved documents were deemed relevant to the user's question.\n"
        "{documents}\n"
        "-----------------------------------------------------------------------------\n"
        "Taking into account the retrieved documents, provide a clear and concise response "
        "to the user's question. Keep your answer factual and refer the user to the sources "
        "when necessary."
        ),
    ]
)

# -----------------------------------------------------------------------------
# Main function to be called in the chat view:

def rag_logic(llm: LLM, vector_store: Chroma, user_query: str) -> tuple[str, list[str]]:
    """Basic RAG logic, retrieves documents, passes them into a prompt,
    and return the answer from the LLM. No verification or validation
    steps.
    
    Args:
        llm (LLM): The LLM to use (can be provided by `initialise_llm()`).
        vector_store (Chroma): The vector DB to use for retrieval (provided
            by `get_vector_db()`).
        user_query (str): The question from the user.
        
    Returns:
        tuple[str, list[str]] - A tuple (final_answer, logic) which contains
        the very last answer provided by the LLM and logic contains all the
        messages sent to the LLM as well as its answers. This traces the
        entire logic of the RAG system.
    """
    # Retrieve the documents:
    documents = chroma_manager.basic_retrieval(user_query, vector_store, 
                                               k = environment.NUM_CHUNKS_TO_RETRIEVE,
                                               threshold = environment.SIMILARITY_THRESHOLD)
    
    if not documents:
        return ("No relevant documents could be retrieved. I cannot answer your question.", [])
    
    # Build the prompt:
    retrieved_str = ""
    for i, doc in enumerate(documents, 1):
        doc = doc[0] # Get rid of the similarity score
        retrieved_str += (
            "-" * 80 + "\n"
            f"Document {i}\n"
            f"Source: {doc.metadata["source"]}\n"
            f"Excerpt: {doc.page_content}\n"
        )
    prompt_value = BASIC_RAG.invoke({"question": user_query, "documents": retrieved_str})
    
    response = llm.invoke(prompt_value)
    return response, [prompt_value.to_messages()]
    
    
# if __name__ == "__main__":
#     import os
#     from ..knowledgebase import chroma_manager
#     from ..llms.init_llm import initialise_llm
#     # Initialise the LLM to be used throughout:
#     llm_to_use = initialise_llm()
#     # Initialise the vector store to be used throughout:
#     vector_store = chroma_manager.get_vector_db(chroma_manager.DEFAULT_COLLECTION_NAME,
#                                                 model_name = environment.EMBEDDING_MODEL,
#                                                 persist_directory = environment.CHROMA_DB_FOLDER + os.sep + "chromadb")
#     result = rag_logic(llm_to_use, vector_store, "What is accessibility?")
#     print(result[0])
#     print(result[1])