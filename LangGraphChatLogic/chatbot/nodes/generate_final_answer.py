"""
This module ends the process.
"""
from LangGraphChatLogic.chatbot.utils.state import OverallState

def generate_final_answer(state: OverallState) -> OverallState:
    """
    Ends the process.

    Args:
        state (OverallState): The state of the question answering process.

    Returns:
        OverallState: The updated state of the question answering process.
    """

    message = "Process complete."
    print(message)
        
    # Create new state with history
    new_state = {
        **state,
        "next_action": "end",
        "final_answer": state.get("final_answer"),
        "step": "generate_final_answer",
        "message": message,
        "all_messages": state.get("all_messages", '') + '\n\n' + message,
        "state_history": state.get("state_history", []) + [{
            "step": "generate_final_answer",
            "message": message,
            "next_action": "end",
        }]
    }
        
    return new_state