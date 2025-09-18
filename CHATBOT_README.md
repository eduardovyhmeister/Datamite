# DATAMITE Chatbot Integration

This document explains how the Chatbot integration is implemented onthe DATAMITE Django application.

## Overview

The chatbot provides assistance with:
- Data monetization concepts and strategies
- ANP-AHP methodology explanations
- Tool usage guidance
- General support for the DATAMITE platform

## Setup Instructions

### 1. Install Dependencies

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Add parameters to .env file
Copy these parameters and add them to the .env-file

#### LLM providers and API keys

LLM_PROVIDER= 'openai' # or 'claude' or 'deepseek', depending which LLM you want to use

OPENAI_API_KEY="YOUR_OPENAI_KEY"
ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_KEY"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_KEY"

#### Name for the vector database
VECTORDB_ID = "NAME_OF_VDB" # the name does not matter, it can be for example "Datamite"
UPLOAD_FOLDER = "YOU_PATH" #Add a path to a file where to save the vector store. For example to the 'LangGraph_chatbot/data/projects' path

#### File to upload
FILE_PATH = "LangGraphChatLogic/data/files/Bub Gizelis Schneider (2025) Towards a Data Monetization Maturtiy Model - AIAI Limassol.pdf"



### 4. Run the Django Application

Start the Django application:

```bash
python manage.py runserver
```
This creates the vector database. The chat can be seen on the right bottom corner.

### 5. Ask questions

Now you can start ask questions

## Chatbot Features

### Pre-built Responses
The chatbot includes responses for:
- Data monetization questions
- ANP-AHP methodology explanations
- Tool usage guidance
- General help and support

### Example Questions
- "What is data monetization?"
- "How does ANP-AHP work?"
- "How do I use the evaluation tool?"
- "What are the benefits of data monetization?"





## Future Enhancements

Potential improvements:
- Connection from the RAGDatamite to the chat interface. To add the use of RAGDatamite see file ANPAHP/views/chat.py and look for #TODO