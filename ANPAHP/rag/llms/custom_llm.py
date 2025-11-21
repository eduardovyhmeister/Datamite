"""A module implementing the langchain interface for LLMs to provide access
to a locally deployed LLM. The main class in this module is `CustomLLM`. You
can create your own class by inheriting from `langchain.llms.base.LLM` and
implementing `_identifying_parameters()` as a property to identify your model
and `_call()` to be used when `invoke()` is called.
"""

from typing import Optional

from langchain.llms.base import LLM
from pydantic import Field
import requests

from utils import environment
from utils import custom_logger as logging
logger = logging.get_logger(__name__, environment.LOGGING_LEVEL)


# -----------------------------------------------------------------------------


class CustomLLM(LLM):
    """A custom LLM that will use a web API of an already deployed LLM model.
    The idea is to make sure we can connect to a locally deployed LLM model and
    use it in the same way as any regular LLM provider.

    Attributes:
        model_name (str): The name used as an ID for your model.
        model_url (str): The URL of the API endpoint to use for your LLM.
        temperature (float): The temperature to use for your LLM.
        max_tokens (int): The maximum number of tokens the LLM can use to answer.
    """
    # Mandatory fields:
    model_name: str = Field(None, alias="model_name")
    model_url: str = Field(None, alias="model_url")
    
    # Optional fields:
    temperature: Optional[float] = 0.5
    max_tokens: Optional[int] = 500
    
    def __init__(self, model_name: str, model_url: str, **kwargs):
        """Constructor of the custom LLM.
        
        Args:
            model_name (str): The name of the model used to identify it.
                Required for tracing purposes. Can be anything, it doesn't
                need to be the name of LLM model used. It's an ID basically.
            model_url (str): The URL of the API endpoint to use.
            
        Kwargs:
            temperature (float): The temperature to use for the LLM (defaults to 0.5).
            max_tokens (int): The number of tokens for the LLM to use when answering (defaults to 500).
        """
        super().__init__()
        self.model_name = model_name
        self.model_url = model_url
        
    @property
    def _identifying_parameters(self):
        """Gets the identifying parameters. Required to be implemented when extending `LLM`.
        This needs to be a property.
        
        Returns:
            dict[str: any] - A dictionary used to identify the model used.
        """
        return {"model_name": self.model_name, "model_url": self.model_url}
    
    @property
    def _llm_parameters(self):
        """Gets the parameters to be sent to the LLM.
        
        Returns:
            dict[str: any] - The parameters to configure the LLM.
        """
        return {"temperature": self.temperature, "max_tokens": self.max_tokens}
    
    @property
    def _llm_type(self):
        """Returns the type of LLM used. Required to extend base.LLM."""
        return "customLLM"
            
    def _call(self, prompt: str, **kwargs) -> str:
        """Method called by `invoke()` in langchain. This is the main logic to get the
        response from the LLM.
        
        Args:
            prompt (str): The prompt to send to the LLM.
        
        Returns:
            str - The response from the LLM.
        """
        content = {
            "prompt": prompt,
            **self._llm_parameters
        }
        try:
            response = requests.post(self.model_url, json = content)
        except Exception as e:
            logger.exception("Could not reach the LLM API.")
            return "An error occurred while trying to reach the LLM, try again later."

        post_response = response.json()
        if response.status_code == 200 and "error" not in post_response:
            return post_response["response"]
        else:
            logger.error(f"Could not reach the LLM API. Error {response.status_code}: {response.text}")
            return "An error occurred while trying to reach the LLM, try again later."
        
