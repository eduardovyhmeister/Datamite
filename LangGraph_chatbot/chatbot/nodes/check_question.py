from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from LangGraph_chatbot.chatbot.utils.llm import llm
from LangGraph_chatbot.chatbot.utils.state import OverallState

class CheckQuestion(BaseModel):

    decision: Literal['TRUE', 'FALSE'] = Field(
        description='Decision on whether the question needs to be decomposed into sub-questions'
    )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are a precise assistant that only breaks down a user question when it is long or complex. If the question is simple, you must not create sub-questions.'
        ),
        (
            'human',
            'You will (1) assess complexity, then (2) optionally produce sub-questions.\n\n'
            'When to break down (any of these true):\n'
            '- The question contains multiple objectives or asks for several outputs.\n'
            '- It requires multi-step reasoning (e.g., gather → compare → decide).\n'
            '- It includes ambiguous terms that need clarification to proceed.\n'
            '- It’s longer than ~30–40 words and has multiple clauses (look for “and/or/then/also/versus”, lists, or nested conditions).\n\n'
            'When NOT to break down:\n'
            '- A single, clear request answerable in one step.\n\n'
            'Rules:\n'
            '- If complex → return "TRUE".\n'
            '- If NOT complex → return "FALSE".\n'
            'Question:\n{query}'
        )
    ]
)

chain = prompt | llm.with_structured_output(CheckQuestion)

def check_question(state: OverallState) -> OverallState:
    """
    Check if the question needs to be decomposed into sub-questions.
    """
    check_question_output = chain.invoke(
        {
            'query': state.get('query')
        }
    )
    if check_question_output.decision == 'TRUE':
        message = 'Question is complex, so the question needs to be decomposed into sub-questions.'
    else:
        message = 'Question is not complex, so document search can be executed directly.'

    print(message)
    new_state = {
        **state,
        'next_action': 'decompose_question' if check_question_output.decision == 'TRUE' else 'first_retrieve_content',
        'step': 'check_question',
        'message': message,
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        'state_history': state.get('state_history', []) + [{
            'step': 'check_question',
            'message': message,
            'next_action': 'decompose_question' if check_question_output.decision == 'TRUE' else 'first_retrieve_content'
        }]
    }
    return new_state
