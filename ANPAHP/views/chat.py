"""Module for views concerning the AI chat system."""

import json
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from ..rag.knowledgebase import chroma_manager
from ..rag.llms.init_llm import initialise_llm
from ..rag.logic.basic_rag import rag_logic
from utils import environment

# Initialise the LLM to be used throughout:
llm_to_use = initialise_llm()
# Initialise the vector store to be used throughout:
vector_store = chroma_manager.get_vector_db(chroma_manager.DEFAULT_COLLECTION_NAME,
                                            model_name = environment.EMBEDDING_MODEL,
                                            persist_directory = environment.CHROMA_DB_FOLDER + os.sep + "chromadb")


@csrf_exempt  # If you prefer CSRF protection, remove this and send X-CSRFToken from JS
@require_POST
def chat_ask_view(request):
    """Accepts a POST with JSON {message}, returns JSON {response, logic}."""
    try:
        body = json.loads(request.body.decode('utf-8')) if request.body else {}
        question = body.get('message', '').strip()
        if not question:
            return JsonResponse({"error": "Empty message"}, status=400)

        response, logic = rag_logic(llm_to_use, vector_store, question)
        return JsonResponse({
            "response": response,
            "logic": logic,
        })
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)

# -----------------------------------------------------------------------------

# Example questions for the chatbot (flat list of strings)
EXAMPLE_QUESTIONS = [
    "What is data monetization?",
    "How does ANP-AHP work?",
    "How do I use the evaluation tool?",
    "What are the benefits of data monetization?"
]

def chat_page(request):
    """View rendering the AI chat window."""
    return render(request, "chat.html", {"example_questions": EXAMPLE_QUESTIONS})

