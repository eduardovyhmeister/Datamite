from .views.chat import EXAMPLE_QUESTIONS


def chatbot_context(_request):
    return {
        "example_questions": EXAMPLE_QUESTIONS,
    }


