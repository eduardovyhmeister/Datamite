#!/usr/bin/env python3
"""
Script to start both the Django server and the Gradio chatbot server.
This is useful for development purposes.
"""

import subprocess
import sys
import os
import time
import signal
import threading

def start_django_server():
    """Start the Django development server"""
    print("Starting Django server...")
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\nDjango server stopped.")
    except Exception as e:
        print(f"Error starting Django server: {e}")

def start_chatbot_server():
    """Start the Gradio chatbot server"""
    print("Starting Gradio chatbot server...")
    try:
        subprocess.run([sys.executable, "chatbot_app.py"], check=True)
    except KeyboardInterrupt:
        print("\nChatbot server stopped.")
    except Exception as e:
        print(f"Error starting chatbot server: {e}")

def main():
    """Main function to start both servers"""
    print("DATAMITE Development Environment")
    print("=" * 40)
    print("Starting both Django and Gradio servers...")
    print("Django will be available at: http://localhost:8000")
    print("Chatbot will be available at: http://localhost:7860")
    print("Press Ctrl+C to stop both servers")
    print("=" * 40)
    
    # Start Django server in a separate thread
    django_thread = threading.Thread(target=start_django_server, daemon=True)
    django_thread.start()
    
    # Give Django a moment to start
    time.sleep(2)
    
    # Start chatbot server in main thread
    try:
        start_chatbot_server()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main() 