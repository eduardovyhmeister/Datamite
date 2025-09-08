#!/usr/bin/env python3
"""
Test script for the DATAMITE Gradio chatbot.
This script tests the chatbot responses without launching the full interface.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_chatbot_responses():
    """Test the chatbot response function"""
    try:
        from chatbot_app import respond
        
        # Test cases
        test_cases = [
            ("What is data monetization?", "data monetization"),
            ("How does ANP work?", "anp"),
            ("How do I use the tool?", "tool"),
            ("I need help", "help"),
            ("Random question", "random")
        ]
        
        print("Testing DATAMITE Chatbot Responses...")
        print("=" * 50)
        
        for question, expected_keyword in test_cases:
            response = respond(question, [])
            print(f"Question: {question}")
            print(f"Response: {response}")
            print(f"Contains '{expected_keyword}': {expected_keyword in response.lower()}")
            print("-" * 30)
        
        print("Chatbot test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"Error importing chatbot: {e}")
        return False
    except Exception as e:
        print(f"Error testing chatbot: {e}")
        return False

if __name__ == "__main__":
    success = test_chatbot_responses()
    sys.exit(0 if success else 1) 