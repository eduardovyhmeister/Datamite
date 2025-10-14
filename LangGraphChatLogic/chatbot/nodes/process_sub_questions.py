'''
This module contains the process_sub_questions node for the chatbot
'''

from LangGraphChatLogic.chatbot.utils.state import OverallState


def process_sub_questions(state: OverallState) -> OverallState:
    """
    Process sub-questions by setting up the current question to be processed.
    This node manages the iteration through multiple decomposed questions.
    """
    
    # Initialize tracking variables if not present
    current_index = state.get('current_question_index', 0)
    sub_questions = state.get('sub_questions', [])
    sub_question_answers = state.get('sub_question_answers', [])
    
    # If this is the first time processing sub-questions, initialize
    if current_index == 0 and len(sub_question_answers) == 0:
        sub_question_answers = []
    
    # Check if we're coming back from validation to increment the index
    next_action = state.get('next_action', '')
    if next_action == 'process_sub_questions':
        # Increment index for next sub-question
        current_index += 1
    
    # Get the current question to process
    if current_index < len(sub_questions):
        current_question = sub_questions[current_index]
        
        # Update state with current question information
        updated_state = state.copy()
        updated_state['current_question_index'] = current_index
        updated_state['current_question'] = current_question
        updated_state['sub_question_answers'] = sub_question_answers
        updated_state['query'] = current_question  # Set the current question as the query for processing
        updated_state['next_action'] = 'first_retrieve_content'
        updated_state['step'] = f'Processing sub-question {current_index + 1} of {len(sub_questions)}: {current_question}'
        
        # Add to state history
        state_history = state.get('state_history', [])
        state_history.append(f"Processing sub-question {current_index + 1}: {current_question}")
        updated_state['state_history'] = state_history
        
        return updated_state
    else:
        # All sub-questions processed, move to composition
        updated_state = state.copy()
        updated_state['next_action'] = 'compose_answer'
        updated_state['step'] = 'All sub-questions processed, composing final answer'
        
        # Add to state history
        state_history = state.get('state_history', [])
        state_history.append("All sub-questions processed, moving to composition")
        updated_state['state_history'] = state_history
        
        return updated_state
