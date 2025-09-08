from langgraph.graph import StateGraph, START, END
from LangGraph_chatbot.chatbot.utils.state import OverallState, InputState, OutputState
from LangGraph_chatbot.chatbot.nodes.decompose_question import decompose_question
from LangGraph_chatbot.chatbot.nodes.first_retrieve_content import first_retrieve_content
from LangGraph_chatbot.chatbot.nodes.generate_first_answer import generate_first_answer
from LangGraph_chatbot.chatbot.nodes.second_retrieve_content import second_retrieve_content
from LangGraph_chatbot.chatbot.nodes.generate_second_answer import generate_second_answer
from LangGraph_chatbot.chatbot.nodes.validation_search import validation_search
from LangGraph_chatbot.chatbot.nodes.compose_answer import compose_answer
from LangGraph_chatbot.chatbot.nodes.generate_final_answer import generate_final_answer
from LangGraph_chatbot.chatbot.nodes.check_question import check_question
from typing import Literal

def chatbot_graph():
    # Create the graph
    langgraph = StateGraph(OverallState, input=InputState, output=OutputState)

    # Add nodes with names
    langgraph.add_node("check_question", check_question)
    langgraph.add_node("decompose_question", decompose_question)
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

    langgraph.add_edge("decompose_question", "first_retrieve_content")

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

    def validation_search_condition(state: OverallState) -> Literal['compose_answer', 'generate_final_answer']:
        if state.get('next_action') == 'compose_answer':
            return 'compose_answer'
        elif state.get('next_action') == 'generate_final_answer':
            return 'generate_final_answer'

    langgraph.add_conditional_edges('validation_search', validation_search_condition)

    langgraph.add_edge('compose_answer', 'generate_final_answer')
    langgraph.add_edge('generate_final_answer', END)

    # Add the graph to the registry
    return langgraph.compile()


