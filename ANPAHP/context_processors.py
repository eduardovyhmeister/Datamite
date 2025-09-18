from ANPAHP import chatbot_examples


def chatbot_context(_request):
    return {
        "example_questions": chatbot_examples.EXAMPLE_QUESTIONS,
    }


