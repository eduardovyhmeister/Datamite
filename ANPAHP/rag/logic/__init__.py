"""All modules related to the RAG logic. If you want to implement your own logic,
create a new module with a function `rag_logic(llm, vector_store, query)` that takes
an initialised LLM as a first argument (obtained through `ANPAHP.rag.llms.init_llm`)
a vector store as a second argument (obtained through 
`ANP.rag.chroma_manager.get_vector_db()`) and the user question as the last argument. 
It should return a tuple (final_answer, logic) where final_answer is a string and 
logic a list of strings reflecting all the prompts sent to the LLM and the answers 
received.

In `views.chat.py`, simply replace the module imported from rag.logic by yours
and it'll handle the rest automatically.
"""