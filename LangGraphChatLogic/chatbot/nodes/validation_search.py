from LangGraphChatLogic.chatbot.utils.state import OverallState
from LangGraphChatLogic.data.vector_store import search_similar_chunks
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from LangGraphChatLogic.chatbot.utils.llm import llm

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
  
    # Check if we're processing sub-questions and need to continue to the next one
    sub_questions = state.get('sub_questions', [])
    current_index = state.get('current_question_index', 0)
    sub_question_answers = state.get('sub_question_answers', [])
    
    # Determine next action based on validation and sub-question status
    if validate_answer_output.decision == 'VALID':
        # Check if we're processing multiple sub-questions
        if len(sub_questions) > 1 and current_index < len(sub_questions):
            # Store the answer for this sub-question
            # Ensure sub_question_answers list is long enough
            while len(sub_question_answers) <= current_index:
                sub_question_answers.append("")
            sub_question_answers[current_index] = state.get('answer_ai_2', '')
            
            # Check if there are more sub-questions to process
            if current_index + 1 < len(sub_questions):
                message = f"Answer for sub-question {current_index + 1} is valid. Moving to next sub-question."
                next_action = 'process_sub_questions'
            else:
                message = "All sub-questions processed. Answer is valid, so the final answer can be composed."
                next_action = 'compose_answer'
        else:
            # Single question or no sub-questions - go directly to composition
            message = "Answer is valid, so the final answer can be composed."
            next_action = 'compose_answer'
    else:
        message = "Answer is incorrect, so the final answer cannot be generated."
        next_action = 'generate_final_answer'

    print(message)
    new_state = {
        **state,
        'next_action': next_action,
        'step': 'validation_search',
        'message': message,
        'sub_question_answers': sub_question_answers,
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        'state_history': state.get('state_history', []) + [{
            'step': 'validation_search',
            'message': message,
            'next_action': next_action
        }]
    }

    return new_state