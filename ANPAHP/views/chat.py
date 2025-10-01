import random
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .. import chatbot_examples as chatbot_examples
from LangGraphChatLogic.chatbot.graph import chatbot_graph

llm_provider = os.getenv('LLM_PROVIDER')


def openai_workflow(question: str):
     
    workflow = chatbot_graph()
    vectorDB_id = os.getenv('VECTORDB_ID')
    result = workflow.invoke({
                "query": question,
                "project_id": vectorDB_id,
                "collection_name": vectorDB_id
            })
    response = result.get('final_answer') or (
                "Unfortunately, an answer could not be found. Please try another question."
        )
    logic = result.get('all_messages') or (
            "AI logic empty"
        )
    return response, logic

def claude_workflow(question: str):
    #TODO: Add the use of RAGDatamite submodule
    pass

def deepseek_workflow(question: str):
    #TODO: Add the use of RAGDatamite submodule
    pass

def chatbot_response(question: str) -> str:

    if "data monetization" in question.lower() or "monetization" in question.lower():
        return random.choice(chatbot_examples.RESPONSES['data_monetization'])
    
    elif "anp" in question.lower() or "ahp" in question.lower():
        return random.choice(chatbot_examples.RESPONSES['anp_ahp'])
    
    elif "tool" in question.lower() or "how to use" in question.lower():
        return random.choice(chatbot_examples.RESPONSES['tool_usage'])
    
    elif "help" in question.lower() or "support" in question.lower():
        return "I'm here to help you understand data monetization and our ANP-AHP tool. You can ask me about data monetization strategies, the ANP-AHP methodology, or how to use our evaluation tool. For detailed instructions, visit the 'How to' section of our website."
    
    else:
        if llm_provider == 'openai':
            response, logic = openai_workflow(question)
   
        #TODO: Add the use of RAGDatamite submodule
        # elif llm_provider == 'claude':
        #     response, logic = claude_workflow(question)
        # elif llm_provider == 'deepseek':
        #     response, logic = deepseek_workflow(question)
        else:
            raise ValueError(f"Invalid LLM provider: {llm_provider}")
        return response, logic


@csrf_exempt  # If you prefer CSRF protection, remove this and send X-CSRFToken from JS
@require_POST
def chat_ask_view(request):
    """Accepts a POST with JSON {message}, returns JSON {response, logic}."""
    try:
        import json
        body = json.loads(request.body.decode('utf-8')) if request.body else {}
        question = body.get('message', '').strip()
        if not question:
            return JsonResponse({"error": "Empty message"}, status=400)

        result = chatbot_response(question)

        if isinstance(result, tuple) and len(result) == 2:
            response, logic = result
        else:
            response = result
            logic = ""

        # Ensure logic is serializable
        if not isinstance(logic, (str, int, float)):
            try:
                import json as _json
                logic = _json.dumps(logic, ensure_ascii=False, indent=2)
            except Exception:
                logic = str(logic)

        return JsonResponse({
            "response": response,
            "logic": logic,
        })
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)


def chat_page(request):
    return render(request, "chat.html", {"example_questions": chatbot_examples.EXAMPLE_QUESTIONS})

