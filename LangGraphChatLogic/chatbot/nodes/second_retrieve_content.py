from LangGraphChatLogic.chatbot.utils.state import OverallState
from LangGraphChatLogic.data.vector_store import search_similar_chunks

def second_retrieve_content(state: OverallState) -> OverallState:
    '''
    Retrieve the content from the vector store with the ai answer
    '''


    project_id = state.get("project_id")
    summary = state.get('summary')

    similar_docs = search_similar_chunks(
        collection_name=project_id,
        questions=[summary],
        project_id=project_id
    )

    formatted_docs = []
    for doc in similar_docs:
        formatted_docs.append({
            'content': doc['text'],
            'metadata': doc['metadata'],
            'relevance': doc['distance']
        })

    if formatted_docs:
        message = "Retrieved relevant document chunks successfully! A second answer can be generated."
    else:
        message = "No relevant document chunks found, an answer cannot be generated."

    print(message)

    new_state = {
        **state,
        'files': formatted_docs,
        'step': 'second_retrieve_content',
        'message': message,
        'next_action': 'generate_second_answer' if formatted_docs else 'generate_final_answer',
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        'state_history': state.get('state_history', []) + [{
            'step': 'second_retrieve_content',
            'message': message,
            'next_action': 'generate_second_answer' if formatted_docs else 'generate_final_answer',
            'files': formatted_docs
        }]
    }

    return new_state