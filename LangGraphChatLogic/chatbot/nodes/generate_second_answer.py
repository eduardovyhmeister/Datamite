from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from LangGraphChatLogic.chatbot.utils.llm import llm
from LangGraphChatLogic.chatbot.utils.state import OverallState

class GenerateAnswerOutput(BaseModel):
    '''
    Structured output for the generate_second_answer node: a well-developed
    answer expanded from the provided summary and retrieved files, plus a
    decision indicating whether a valid answer can be generated.
    '''
    answer: str = Field(
        description='Expanded answer based on retrieved content (with citations where appropriate)'
    )
 

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that writes clear and professional explanations based on summaries and retrieved content from relevant files."
        ),
        (
            "human",
            (
                "You are provided with:\n"
                "- A short summary describing the main point\n"
                "- Retrieved content from relevant files\n\n"
                "Your task is to write a longer, well-developed answer based on the retrieved content.\n"
                "Use the summary as a guide for what the answer should focus on.\n"
                "Only include information that is supported by the retrieved content.\n"
                "If some parts of the summary cannot be supported, exclude them and focus on what the documents confirm.\n\n"
                "Include citations to the supporting files and chunk numbers where appropriate (e.g., 'document.pdf, chunk 2').\n"
                "Write the answer in a professional tone, as it would appear in a formal report.\n\n"
                "Retrieved content:\n{files}\n\n"
                "Summary to expand:\n{summary}\n\n"
                "Return fields:\n"
                "- answer: the expanded answer based on the retrieved content (with citations where appropriate)\n"
            )
        )
    ]
)



chain = prompt | llm.with_structured_output(GenerateAnswerOutput)

def generate_second_answer(state:OverallState) -> OverallState:
    '''
    Generates and summarises the answer from the sub-questions
    '''

    generate_answer_output = chain.invoke(
        {
            'summary': state.get('summary'),
            'files': state.get('files')
        }
    )


    message = "Answer was generated! Both of the answers need to be validated to ensure they are aligned."
 
    print(message)

    new_state = {
        **state,
        "next_action":  "validation_search",
        "answer_ai_2": generate_answer_output.answer,
        "step": "generate_second_answer",
        "message": message,
        "all_messages": state.get("all_messages", '') + '\n\n' + message,
        "state_history": state.get("state_history", []) + [{
            "step": "generate_second_answer",
            "message": message,
            "next_action": "validation_search",
            "answer_ai_2": generate_answer_output.answer if generate_answer_output.answer else None
        }]
    }

    return new_state

