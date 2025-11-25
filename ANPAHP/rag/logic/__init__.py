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

For example, you can create a new file under `ANPAHP.rag.logic` called `my_logic.py`.
Here is the minimal content of the file:

```
from chromadb import Collection
from langchain.llms.base import LLM
from langchain_core.prompts import ChatPromptTemplate

def rag_logic(llm: LLM, vector_store: Collection, user_query: str) -> tuple[str, list[str]]:
    return "test", ["This is test logic A", "This is test logic B"]
```

Once this file is done, simple go into `ANPAHP.views.chat.py` and replace the import from
rag logic with your new file.
"""