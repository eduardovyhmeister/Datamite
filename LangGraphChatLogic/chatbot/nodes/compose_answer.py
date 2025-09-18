from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from LangGraphChatLogic.chatbot.utils.state import OverallState
from LangGraphChatLogic.chatbot.utils.llm import llm
from pydantic import BaseModel, Field
from typing import Literal

class GenerateAnswerOutput(BaseModel):
    '''
    Class for the output of the compose_answer node
    '''
    answer: str = Field(
        description='Final answer to the question'
    )


# Define the prompt using your desired language
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert chatbot assistant. Given two different AI-generated answers to a user question, "
        "combine them into a single, well-structured and clear answer."
    ),
    (
        "human",
        (
            "Your task is to:\n"
            "1. Review both drafts.\n"
            "2. Compose a clear, concise, and professional final answer that incorporates the best parts of each.\n"
            "3. Ensure the tone matches the style of the original question.\n"
            "4. Avoid repetition and contradictions.\n"
            "5. Phrase the result formally.\n\n"
            "If the drafts disagree or one lacks clarity, improve the text accordingly without losing important meaning.\n\n"
            "Question:\n{query}\n\n"
            "Draft Answer 1:\n{answer_ai_1}\n\n"
            "Draft Answer 2:\n{answer_ai_2}\n\n"
            "Final Composed Answer:"
        )
    )
])

# Chain
chain = prompt | llm.with_structured_output(GenerateAnswerOutput)

# Compose node
def compose_answer(state: OverallState) -> OverallState:
    """
    Compose the final answer from two AI-generated drafts using a structured ChatPromptTemplate.
    """
    answer_ai_1 = state.get("answer_ai_1", "")
    answer_ai_2 = state.get("answer_ai_2", "")
    query = state.get("query")

    response = chain.invoke({
        "query": query,
        "answer_ai_1": answer_ai_1,
        "answer_ai_2": answer_ai_2,
    })

    message = "Answer was generated succesfully."
    print(message)

    new_state = {
        **state,
        'final_answer': response.answer,
        'step': 'compose_answer',
        'message': message,
        'next_action': 'generate_final_answer',
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        'state_history': state.get('state_history', []) + [{
            'step': 'compose_answer',
            'message': message,
            'next_action': 'generate_final_answer',
            'final_answer': response.answer
        }]
    }
    return new_state


