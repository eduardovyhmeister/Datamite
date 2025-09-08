from LangGraph_chatbot.chatbot.utils.state import OverallState
from LangGraph_chatbot.data.vector_store import search_similar_chunks

def first_retrieve_content(state: OverallState) -> OverallState:
    '''
    Retrieve the content from the vector store
    '''
    project_id = state.get("project_id")
    sub_questions = state.get('sub_questions')
    if sub_questions:
        all_questions = [state.get('query')] + sub_questions
    else:
        all_questions = [state.get('query')]


    similar_docs = search_similar_chunks(
        collection_name=project_id,
        questions=all_questions,
        project_id=project_id
    )

    formatted_docs = []
    for doc in similar_docs:
        formatted_docs.append({
            'content': doc['text'],
            'metadata': doc['metadata'],
            'relevance': doc['distance']
        })

    message = "Retrieved relevant document chunks successfully! An answer can be generated." if formatted_docs else "No relevant document chunks found, an answer cannot be generated."
    print(message)
    
    new_state = {
        **state,
        'files': formatted_docs,
        'step': 'first_retrieve_content',
        'message': message,
        'next_action': 'generate_first_answer' if formatted_docs else 'generate_final_answer',
        'all_messages': state.get('all_messages', '') + '\n\n' + message,
        'state_history': state.get('state_history', []) + [{
            'step': 'first_retrieve_content',
            'message': message,
            'next_action': 'generate_first_answer' if formatted_docs else 'generate_final_answer',
            'files': formatted_docs
        }]
    }

    return new_state
