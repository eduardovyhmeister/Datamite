#!/usr/bin/env python3
"""
Script to run the Gradio chatbot server for DATAMITE.
This should be run separately from the Django application.
"""

import subprocess
import sys
import os
from LangGraph_chatbot.data.document_handling import load_project_documents

def main():
    """Run the Gradio chatbot server"""
    print("Starting DATAMITE Gradio Chatbot Server...")
    print("Data will be loaded to the Chatbot's vector store")
    print("The chatbot will be available at: http://localhost:7860")
    print("Press Ctrl+C to stop the server")

    project_id = "test_project"
    files_to_process = ["LangGraph_chatbot/data/files/Bub Gizelis Schneider (2025) Towards a Data Monetization Maturtiy Model - AIAI Limassol.pdf"]
    try:
        load_project_documents(project_id=project_id, files_to_process=files_to_process, collection_name=project_id)
    except Exception as e:
        print(f"Error loading documents to vector store: {e}")
    try:
        # Run the chatbot app
        subprocess.run([sys.executable, "chatbot_app.py"])

    except KeyboardInterrupt:
        print("\nChatbot server stopped.")
    except Exception as e:
        print(f"Error running chatbot server: {e}")

if __name__ == "__main__":
    main() 