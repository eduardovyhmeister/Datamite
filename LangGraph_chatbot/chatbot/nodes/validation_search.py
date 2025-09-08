from LangGraph_chatbot.chatbot.utils.state import OverallState
from LangGraph_chatbot.data.vector_store import search_similar_chunks
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from LangGraph_chatbot.chatbot.utils.llm import llm

class ValidateAnswerOutput(BaseModel):

    decision: Literal['VALID', 'INCORRECT'] = Field(
        description='Decision on whether the answer is valid'
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that compares two AI-generated answers. "
            "Your goal is to determine whether the answers are broadly aligned in meaning and outcome, based on the retrieved content."
        ),
        (
            "human",
            (
                "You are given:\n"
                "- The original user question\n"
                "- Two AI-generated answers\n"
                "- Retrieved content from related files (used to generate the answers)\n\n"
                "Your task is to check whether both answers:\n"
                "1. Are generally consistent with the retrieved content\n"
                "2. Lead to a similar overall conclusion or outcome\n"
                "3. Are phrased in a reasonably clear and professional way\n\n"
                "The answers do not need to be identical or cover the exact same details — just make sure they are broadly similar and could both be used to answer the question.\n\n"
                "**Your response must include:**\n"
                "- `decision`: Use 'VALID' if both answers are similar enough to be considered aligned. Use 'INCORRECT' if one clearly contradicts the other or is unsupported.\n"
                "- `correction_steps`: If the decision is 'INCORRECT', list what needs to be fixed (e.g., 'Answer 1 needs to match the conclusion of Answer 2', 'Answer 2 needs a citation'). If 'VALID', return an empty list.\n\n"
                "Retrieved content:\n{files}\n\n"
                "Question:\n{query}\n\n"
                "Answer 1:\n{answer_ai_1}\n\n"
                "Answer 2:\n{answer_ai_2}\n"
            )
        ),
    ]
)



chain= prompt | llm.with_structured_output(ValidateAnswerOutput)


def validation_search(state: OverallState) -> OverallState:
    '''
    Validate the summarised result by retrieving the content from the vector store
    '''


    validate_answer_output = chain.invoke(
        {
            'query': state.get('query'),
            'files': state.get('files'),
            'answer_ai_1': state.get('answer_ai_1'),
            'answer_ai_2': state.get('answer_ai_2')
        }
    )
  
    if validate_answer_output.decision == 'VALID':
        message = "Answer is valid, so the final answer can be composed."
    else:
        message = "Answer is incorrect, so the final answer cannot be generated."

    print(message)
    new_state = {
        **state,
        'next_action': 'compose_answer' if validate_answer_output.decision == 'VALID' else 'generate_final_answer',
        'step': 'validation_search',
        'message': message,
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        'state_history': state.get('state_history', []) + [{
            'step': 'validation_search',
            'message': message,
            'next_action': 'compose_answer' if validate_answer_output.decision == 'VALID' else 'generate_final_answer'
        }]
    }

    return new_state