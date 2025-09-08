import gradio as gr
import random
from chatbot_config import RESPONSES, EXAMPLE_QUESTIONS, CURRENT_CONFIG
from LangGraph_chatbot.chatbot.graph import chatbot_graph

workflow = chatbot_graph()


def respond(message, history):
    """Simple chatbot response function"""
    project_id = "test_project"
    # Simple keyword-based responses
    if "data monetization" in message.lower() or "monetization" in message.lower():
        return random.choice(RESPONSES['data_monetization'])
    
    elif "anp" in message.lower() or "ahp" in message.lower():
        return random.choice(RESPONSES['anp_ahp'])
    
    elif "tool" in message.lower() or "how to use" in message.lower():
        return random.choice(RESPONSES['tool_usage'])
    
    elif "help" in message.lower() or "support" in message.lower():
        return "I'm here to help you understand data monetization and our ANP-AHP tool. You can ask me about data monetization strategies, the ANP-AHP methodology, or how to use our evaluation tool. For detailed instructions, visit the 'How to' section of our website."
    
    else:
        result = workflow.invoke({
                "query": message,
                "project_id": project_id,
                "collection_name": project_id
            })
        response = result.get('final_answer') or (
                "Unfortunately, an answer could not be found. Please try another question."
        )
        logic = result.get('all_messages') or (
            "AI logic empty"
        )
        
        return response, logic



# Create the Gradio interface


with gr.Blocks(
    fill_height=True,          # makes the app at least viewport-height
    css="""
html, body, .gradio-container { height: 100%; }

/* Top-level page container */
#page { min-height: 100dvh; }                /* modern browsers */
@supports not (height: 100dvh) {
  #page { min-height: 100vh; }               /* fallback */
}

/* Make the main row fill the page height */
#mainrow { height: 100%; align-items: stretch; }

/* Columns act as vertical flex boxes so children can fill */
#chat-col, #logic-col { display: flex; flex-direction: column; }

/* Logic panel fills its column and scrolls */
#logic-panel { flex: 1; overflow: auto; border: 1px solid #eee; padding: 10px; border-radius: 10px; }
"""
) as demo:
    with gr.Row(elem_id="mainrow", equal_height=True):
        # Logic column (created first so we can pass it to additional_outputs)
        with gr.Column(scale=1,elem_id="logic-col"):
            with gr.Accordion("AI Logic", open=True):
                logic_md = gr.Markdown("(AI logic will appear here)", elem_id="logic-panel")

        with gr.Column(scale=5, elem_id="chat-col"):
            gr.ChatInterface(
                fn=respond,
                type="messages",
                title="DATAMITE Data Monetization Assistant",
                description="Ask me about data monetization, ANP-AHP methodology, or how to use our evaluation tool!",
                examples=EXAMPLE_QUESTIONS,
                theme=gr.themes.Soft(),
                additional_outputs=[logic_md], 
            )

if __name__ == "__main__":
    demo.launch(
        server_name=CURRENT_CONFIG['server_name'],
        server_port=CURRENT_CONFIG['server_port'],
        share=CURRENT_CONFIG['share'],
        debug=CURRENT_CONFIG['debug']
    ) 