'''
This module containes the used states for the chatbot
'''

from typing import List, TypedDict


class InputState(TypedDict):
    '''
    InputState is a dictionary with the following keys:
    '''
    query: str
    project_id: str
    collection_name: str

class OverallState(TypedDict):
    '''
    OverallState is a dictionary with the following keys:
    '''

    project_id: str
    collection_name: str
    query: str
    sub_questions: List[str]
    current_question_index: int
    current_question: str
    sub_question_answers: List[str]
    summary: str
    answer_ai_1: str
    answer_ai_2: str
    final_answer: str
    files = List[dict]
    correction_steps: List[str]
    rejection_reasons: List[str]
    next_action: str
    step: str
    message: str
    all_messages: str
    state_history: List[str]


class OutputState(TypedDict):
    '''
    OutputState is a dictionary with the following keys:
    '''
    final_answer: str
    files: List[dict]
    correction_steps: List[str]
    rejection_reasons: List[str]
    step: str
    message: str
    all_messages: str
    state_history: List[dict]


