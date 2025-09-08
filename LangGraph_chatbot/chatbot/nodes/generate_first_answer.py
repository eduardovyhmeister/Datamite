from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from LangGraph_chatbot.chatbot.utils.llm import llm
from LangGraph_chatbot.chatbot.utils.state import OverallState

class GenerateAnswerOutput(BaseModel):
    '''
    Class for the output of the summarise_result node
    '''
    answer: str = Field(
        description='Answer to the subquestions'
    )
    summary: str = Field(
        description='Brief summary of the answer, approximately 1-2 sentences'
    )
    decision: Literal['ANSWER', 'NO ANSWER'] = Field(
        description="Decision on whether the answer can be generated"
    )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that answers user questions using content retrieved from relevant files. "
            "You respond clearly, professionally, and match the tone of the user's original query."
        ),
        (
            "human",
            (
                "You are given:\n"
                "- A user question (original query)\n"
                "- A set of sub-questions that break it down\n"
                "- Retrieved content from related files\n\n"
                "Your task is to:\n"
                "1. Answer the **original query** as clearly and professionally as possible. You may use the sub-questions to guide your thinking, but do not treat them as mandatory.\n"
                "2. Include supporting citations when possible (e.g., 'document.pdf, chunk 2').\n"
                "3. After writing the full answer, generate a **brief summary** of the answer (1–2 sentences) highlighting the key point(s).\n"
                "4. Decide whether the answer can be generated based on the retrieved content.\n\n"
                "**Important:**\n"
                "- Do not say that no relevant content was found unless you have carefully reviewed the retrieved text.\n"
                "- Keep the full answer concise and suitable for a formal report.\n\n"
                "**Return the following fields:**\n"
                "- `answer`: Full professional answer based on the retrieved content\n"
                "- `summary`: 1–2 sentence summary of the answer\n"
                "- `decision`: 'ANSWER' if an answer can be produced, otherwise 'NO ANSWER'\n\n"
                "Retrieved content:\n{files}\n\n"
                "Sub-questions:\n{sub_questions}\n\n"
                "Original query:\n{query}"
            )
        )
    ]
)





chain = prompt | llm.with_structured_output(GenerateAnswerOutput)

def generate_first_answer(state:OverallState) -> OverallState:
    '''
    Generates and summarises the answer from the sub-questions
    '''

    generate_answer_output = chain.invoke(
        {
            'query': state.get('query'),
            'files': state.get('files'),
            'sub_questions': state.get('sub_questions')
        }
    )
    answer = generate_answer_output.answer
    answer = answer.replace('-\n', '')
    answer = answer.replace('\n', ' ')

    if generate_answer_output.decision == 'ANSWER':
        message = "Answer generated successfully! A summary of this answer has been generated and it is used for the second document search."
    else:
        message = "Answer can not be generated, so the final answer cannot be generated."

    print(message)

    new_state = {
        **state,
        "next_action": "generate_final_answer" if generate_answer_output.decision == "NO ANSWER" else "second_retrieve_content",
        "summary": generate_answer_output.summary if generate_answer_output.summary else None,
        "answer_ai_1": answer if answer else None,
        "step": "generate_first_answer",
        "message": message,
        "all_messages": state.get("all_messages", '') + '\n\n' + message,
        "state_history": state.get("state_history", []) + [{
            "step": "generate_first_answer",
            "message": message,
            "next_action": "generate_final_answer" if generate_answer_output.decision == "NO ANSWER" else "second_retrieve_content",
            "answer_ai_1": answer if answer else None,
            "summary": generate_answer_output.summary if generate_answer_output.summary else None
        }]
    }

    return new_state

