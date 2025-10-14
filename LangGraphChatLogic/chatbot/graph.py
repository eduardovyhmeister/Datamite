from langgraph.graph import StateGraph, START, END
from LangGraphChatLogic.chatbot.utils.state import OverallState, InputState, OutputState
from LangGraphChatLogic.chatbot.nodes.decompose_question import decompose_question
from LangGraphChatLogic.chatbot.nodes.process_sub_questions import process_sub_questions
from LangGraphChatLogic.chatbot.nodes.first_retrieve_content import first_retrieve_content
from LangGraphChatLogic.chatbot.nodes.generate_first_answer import generate_first_answer
from LangGraphChatLogic.chatbot.nodes.second_retrieve_content import second_retrieve_content
from LangGraphChatLogic.chatbot.nodes.generate_second_answer import generate_second_answer
from LangGraphChatLogic.chatbot.nodes.validation_search import validation_search
from LangGraphChatLogic.chatbot.nodes.compose_answer import compose_answer
from LangGraphChatLogic.chatbot.nodes.generate_final_answer import generate_final_answer
from LangGraphChatLogic.chatbot.nodes.check_question import check_question
from typing import Literal

def chatbot_graph():
    # Create the graph
    langgraph = StateGraph(OverallState, input=InputState, output=OutputState)

    # Add nodes with names
    langgraph.add_node("check_question", check_question)
    langgraph.add_node("decompose_question", decompose_question)
    langgraph.add_node("process_sub_questions", process_sub_questions)
    langgraph.add_node("first_retrieve_content", first_retrieve_content)
    langgraph.add_node("generate_first_answer", generate_first_answer)
    langgraph.add_node("second_retrieve_content", second_retrieve_content)
    langgraph.add_node("generate_second_answer", generate_second_answer)
    langgraph.add_node("validation_search", validation_search)
    langgraph.add_node("compose_answer", compose_answer)
    langgraph.add_node('generate_final_answer', generate_final_answer)

    # Add edges
    langgraph.add_edge(START, "check_question")

    def check_question_condition(state: OverallState) -> Literal['decompose_question', 'first_retrieve_content']:
        if state.get('next_action') == 'decompose_question':
            return 'decompose_question'
        elif state.get('next_action') == 'first_retrieve_content':
            return 'first_retrieve_content'
        
    langgraph.add_conditional_edges('check_question', check_question_condition)

    def decompose_question_condition(state: OverallState) -> Literal['process_sub_questions', 'first_retrieve_content']:
        # Use the next_action determined by the decompose_question node
        next_action = state.get('next_action', 'first_retrieve_content')
        if next_action == 'process_sub_questions':
            return 'process_sub_questions'
        else:
            return 'first_retrieve_content'
        
    langgraph.add_conditional_edges('decompose_question', decompose_question_condition)

    def process_sub_questions_condition(state: OverallState) -> Literal['first_retrieve_content', 'compose_answer']:
        # Check if we've processed all sub-questions
        current_question_index = state.get('current_question_index', 0)
        sub_questions = state.get('sub_questions', [])
        
        if current_question_index < len(sub_questions):
            return 'first_retrieve_content'
        else:
            return 'compose_answer'
        
    langgraph.add_conditional_edges('process_sub_questions', process_sub_questions_condition)

    def first_retrieve_content_condition(state: OverallState) -> Literal['generate_first_answer', 'generate_final_answer']:
        if state.get('next_action') == 'generate_first_answer':
            return 'generate_first_answer'
        elif state.get('next_action') == 'generate_final_answer':
            return 'generate_final_answer'
        
    langgraph.add_conditional_edges('first_retrieve_content', first_retrieve_content_condition)

    langgraph.add_edge('generate_first_answer', 'second_retrieve_content')

    def second_retrieve_content_condition(state: OverallState) -> Literal['generate_second_answer', 'generate_final_answer']:
        if state.get('next_action') == 'generate_second_answer':
            return 'generate_second_answer'
        elif state.get('next_action') == 'generate_final_answer':
            return 'generate_final_answer'
        
    langgraph.add_conditional_edges('second_retrieve_content', second_retrieve_content_condition)

    langgraph.add_edge('generate_second_answer', 'validation_search')

    def validation_search_condition(state: OverallState) -> Literal['compose_answer', 'generate_final_answer', 'process_sub_questions']:
        if state.get('next_action') == 'compose_answer':
            return 'compose_answer'
        elif state.get('next_action') == 'generate_final_answer':
            return 'generate_final_answer'
        elif state.get('next_action') == 'process_sub_questions':
            return 'process_sub_questions'

    langgraph.add_conditional_edges('validation_search', validation_search_condition)

    langgraph.add_edge('compose_answer', 'generate_final_answer')
    langgraph.add_edge('generate_final_answer', END)

    # Add the graph to the registry
    return langgraph.compile()


