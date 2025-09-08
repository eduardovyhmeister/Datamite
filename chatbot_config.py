"""
Configuration file for the DATAMITE Gradio chatbot.
Modify these settings based on your environment.
"""

import os

# Chatbot server configuration
CHATBOT_CONFIG = {
    # Development settings
    'development': {
        'server_name': '0.0.0.0',
        'server_port': 7860,
        'share': True,
        'debug': True,
        'iframe_url': 'http://localhost:7860'
    },
    
    # Production settings
    'production': {
        'server_name': '0.0.0.0',
        'server_port': 7860,
        'share': False,
        'debug': False,
        'iframe_url': 'https://your-production-domain.com:7860'  # Update this
    }
}

# Get current environment (default to development)
ENVIRONMENT = os.getenv('DATAMITE_ENV', 'development')

# Current configuration
CURRENT_CONFIG = CHATBOT_CONFIG[ENVIRONMENT]

# Chatbot responses configuration
RESPONSES = {
    'data_monetization': [
        "Data monetization involves creating value from your data through improved efficiency, better decision-making, or new revenue streams.",
        "Data monetization is the process of creating value from your data assets. This can include improving operational efficiency, enhancing decision-making processes, or creating entirely new revenue streams. Our ANP-AHP tool helps you evaluate different aspects of data monetization systematically."
    ],
    
    'anp_ahp': [
        "The ANP-AHP methodology helps you evaluate and prioritize different aspects of data monetization strategies.",
        "ANP (Analytic Network Process) and AHP (Analytic Hierarchy Process) are decision-making methodologies that help you prioritize and evaluate complex decisions using mathematical and psychological principles. Our tool combines these with the Balanced Scorecard approach for data monetization evaluation."
    ],
    
    'tool_usage': [
        "You can start by identifying your key performance indicators (KPIs) and objectives for data monetization.",
        "Our ANP-AHP tool guides you through a structured process to evaluate data monetization strategies. You can start by creating an evaluation, defining objectives, setting KPIs, and then comparing different criteria to determine priorities. Check out the 'How to' section for detailed instructions!"
    ],
    
    'general': [
        "The Balanced Scorecard approach helps align your data strategy with overall business objectives.",
        "Would you like to learn more about how to use our ANP-AHP tool for data monetization evaluation?",
        "Data quality, accessibility, and business impact are key factors in data monetization success.",
        "Our tool can help you compare different datasets and evaluate their potential value for your business.",
        "The DATAMITE project focuses on European perspectives for data monetization strategies."
    ]
}

# Example questions for the chatbot
EXAMPLE_QUESTIONS = [
    ["What is data monetization?"],
    ["How does ANP-AHP work?"],
    ["How do I use the evaluation tool?"],
    ["What are the benefits of data monetization?"]
] 