from LangGraphChatLogic.chatbot.utils.state import InputState, OverallState
from LangGraphChatLogic.chatbot.utils.llm import llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

class DecomposeQuestionOutput(BaseModel):
    sub_questions: List[str] = Field(
        description="List of decomposed sub-questions"
    )

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that breaks down long andcomplex questions into smaller, logically connected parts."),
    ("human", 
     "If the question is long and complex, please break it into 1–5 simpler sub-questions that are directly related to the original.\n"
     "Your task is not to generate new questions, but to break down the original question into smaller, more specific questions.\n\n"
     "Question:\n{query}")
])

chain = prompt | llm.with_structured_output(DecomposeQuestionOutput)

def decompose_question(state: OverallState) -> OverallState:
    """
    Decompose a question into sub-questions using structured LLM output.
    """

    query = state.get("query")

    result = chain.invoke({"query": query})


    # Determine if we need to process sub-questions or go directly to content retrieval
    if len(result.sub_questions) > 1:
        message = f"Question decomposed into {len(result.sub_questions)} sub-questions."
        next_action = 'process_sub_questions'
    elif len(result.sub_questions) == 1:
        message = "Question decomposed into 1 sub-question. Processing directly."
        next_action = 'first_retrieve_content'
        # Set the single sub-question as the current query
        state['query'] = result.sub_questions[0]
    else:
        message = "Question could not be decomposed. Processing original question directly."
        next_action = 'first_retrieve_content'
    
    print(message)

    new_state = {
        **state,
        "sub_questions": result.sub_questions,
        "step": "decompose_question",
        "message": message,
        'next_action': next_action,
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        "state_history": state.get("state_history", []) + [{
            "step": "decompose_question",
            "message": message,
            "sub_questions": result.sub_questions
        }]
    }

    return new_state