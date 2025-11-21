"""A small module just to initiate the supported LLMs.
To get the LLM to be used, just call `initialise_llm()` and
it'll return an LLM object.
"""

from langchain.llms.base import LLM
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek

from . import custom_llm

# Get the logger for the file processors.
from utils import environment
from utils import custom_logger as logging
logger = logging.get_logger(__name__, environment.LOGGING_LEVEL)


# -----------------------------------------------------------------------------

def initialise_llm() -> LLM :
    """Initiate the LLM to be used with the RAG system, based on the environment
    set."""
    llm_to_use = environment.LLM_SERVICE_PROVIDER
    
    if not llm_to_use:
        logger.error("Could not initiate the LLM since no service provider was set in the environment.")
        return None
    
    if llm_to_use == "openai":
        return ChatOpenAI(model = environment.LLM_MODEL,
                          temperature = environment.LLM_TEMPERATURE,
                          max_completion_tokens = environment.LLM_MAX_TOKENS,
                          api_key = environment.LLM_API_KEY)
    elif llm_to_use == "claude":
        return ChatAnthropic(model_name = environment.LLM_MODEL,
                             temperature = environment.LLM_TEMPERATURE,
                             max_tokens_to_sample = environment.LLM_MAX_TOKENS,
                             api_key = environment.LLM_API_KEY)
    elif llm_to_use == "deepseek":
        return ChatDeepSeek(model = environment.LLM_MODEL,
                            temperature = environment.LLM_TEMPERATURE,
                            max_tokens = environment.LLM_MAX_TOKENS,
                            api_key = environment.LLM_API_KEY)
    elif llm_to_use == "custom":
        return custom_llm.CustomLLM(model_name = environment.LLM_MODEL,
                                   temperature = environment.LLM_TEMPERATURE,
                                   max_tokens_to_sample = environment.LLM_MAX_TOKENS,
                                   model_url = environment.LLM_URL)
    else:
        logger.error(f"The selected service provider '{environment.LLM_SERVICE_PROVIDER}' is not supported yet.")
        return None