"""
This module contains the LLM configuration for answer-drafting.

The LLM is configured using the ChatOpenAI class from the langchain_openai library.
The model used is gpt-4o with a temperature of 0.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from LangGraphChatLogic.data.data_config import LLM_TEMPERATURE
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o", temperature=LLM_TEMPERATURE)