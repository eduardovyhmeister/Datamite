"""A module that loads the .env file when imported. This is used to keep
a single place where all the default values for the environment variables
are set. The environment variables are then provided as constants. They
are already typecast correctly, and only valid values can be provided here.

For more information about the environment variables used by the projects,
please have a look at .env.template which provides a template for setting
the required environment variables, with instructions on how to set them
up.

WARNING: If you edit the constants provided here later on in your code, 
then you're making your own bed."""

import os
import sys
from typing import Any

import dotenv

from . import custom_logger as logging

# -----------------------------------------------------------------------------
# Default values for the environment variables, mandatory variables
# are set to `None` by default. You can set the default values here
# by simply changing the value.
LOGGING_LEVEL = "info"

DJANGO_SECRET_KEY = None
DJANGO_DEBUG = None
DJANGO_ALLOWED_HOSTS = None

LLM_DISABLE = 0
LLM_TEMPERATURE = 0.5
LLM_MAX_TOKENS = 1000
LLM_SERVICE_PROVIDER = None
LLM_API_KEY = None
LLM_MODEL = None
LLM_URL = None

CHROMA_DB_FOLDER = "."
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
KNOWLEDGE_FOLDERS = None
KNOWLEDGE_SEARCH_RECURSIVELY = 0
KNOWLEDGE_FILE_TYPES = ""
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# -----------------------------------------------------------------------------
# Actually loading the environment:
dotenv.load_dotenv()
errors = 0
warning_msg = "Environment variable '{}' was not set to a supported value, it was thus set to the default value '{1}'."
error_msg = "Environment variable '{0}' was not set properly. Please have a look at .env.template for more information."

# TODO: Could use generic functions to load the environment but I can't be bothered.

# -----------------
try:
    LOGGING_LEVEL = logging.LOG_LEVELS[os.environ.get("LOGGING_LEVEL", LOGGING_LEVEL).lower()]
    raise_warning = False
except KeyError:
    raise_warning = True
    
logger = logging.get_logger(__name__, level = LOGGING_LEVEL)
if raise_warning:
    logger.warning(warning_msg.format('LOGGING_LEVEL', 'info'))

# -----------------
DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", DJANGO_SECRET_KEY)
if not DJANGO_SECRET_KEY:
    logger.error(error_msg.format("DJANGO_SECRET_KEY"))
    errors += 1

# -----------------
try:
    DJANGO_DEBUG = int(os.environ.get("DEBUG", DJANGO_DEBUG))
except ValueError:
    logger.error(error_msg.format("DEBUG"))
    errors += 1

# -----------------
try:
    DJANGO_ALLOWED_HOSTS = [host.strip() 
                            for host in os.environ.get("ALLOWED_HOSTS", DJANGO_ALLOWED_HOSTS).split(',')
                            if host.strip()]
except AttributeError:
    logger.error(error_msg("ALLOWED_HOSTS"))
    errors += 1
    
# -----------------
try:
    LLM_DISABLE = int(os.environ.get("LLM_DISABLE", LLM_DISABLE))
except ValueError:
    logger.warning(warning_msg.format("LLM_DISABLE", LLM_DISABLE))
    
# -----------------
try:
    LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", LLM_TEMPERATURE))
except ValueError:
    logger.warning(warning_msg.format("LLM_TEMPERATURE", LLM_TEMPERATURE))

# -----------------
try:
    LLM_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", LLM_MAX_TOKENS))
except ValueError:
    logger.warning(warning_msg.format("LLM_MAX_TOKENS", LLM_MAX_TOKENS))
    
# -----------------
LLM_SERVICE_PROVIDER = os.environ.get("LLM_SERVICE_PROVIDER").lower()
if LLM_SERVICE_PROVIDER not in ["openai", "anthropic", "deepseek", "custom"]:
    logger.error(error_msg.format("LLM_SERVICE_PROVIDER"))
    errors += 1

# -----------------
if LLM_SERVICE_PROVIDER == "custom":
    LLM_URL = os.environ.get("LLM_URL", LLM_URL)
    if not LLM_URL:
        logger.error(error_msg.format("LLM_URL"))
        errors += 1
else:
    LLM_API_KEY = os.environ.get("LLM_API_KEY", LLM_API_KEY)
    if not LLM_API_KEY:
        logger.error(error_msg.format("LLM_API_KEY"))
        errors += 1
    
    LLM_MODEL = os.environ.get("LLM_MODEL", LLM_MODEL)
    if not LLM_MODEL:
        logger.error(error_msg.format("LLM_MODEL"))
        errors += 1
    
# -----------------
CHROMA_DB_FOLDER = os.environ.get("CHROMA_DB_FOLDER", CHROMA_DB_FOLDER)
if not CHROMA_DB_FOLDER:
    logger.warning(warning_msg.format("CHROMA_DB_FOLDER"))
    
# -----------------
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", EMBEDDING_MODEL)
if not EMBEDDING_MODEL:
    logger.warning(warning_msg.format("EMBEDDING_MODEL"))
    
# -----------------
try:
    KNOWLEDGE_FOLDERS = [folder.strip()
                         for folder in os.environ.get("KNOWLEDGE_FOLDERS").split(',')
                         if folder.strip()]
except AttributeError:
    logger.error(error_msg.format("KNOWLEDGE_FOLDERS"))
    errors += 1
    
# -----------------
try:
    KNOWLEDGE_SEARCH_RECURSIVELY = int(os.environ.get("KNOWLEDGE_SEARCH_RECURSIVELY", KNOWLEDGE_SEARCH_RECURSIVELY))
except ValueError:
    logger.warning(warning_msg.format("KNOWLEDGE_SEARCH_RECURSIVELY", KNOWLEDGE_SEARCH_RECURSIVELY))
    
# -----------------
try:
    KNOWLEDGE_FILE_TYPES = [extension.strip()
                            for extension in os.environ.get("KNOWLEDGE_FILE_TYPES", KNOWLEDGE_FILE_TYPES).split(',')
                            if extension.strip()]
except AttributeError:
    logger.warning(warning_msg.format("KNOWLEDGE_FILE_TYPES", KNOWLEDGE_FILE_TYPES))

# -----------------
try:
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", CHUNK_SIZE))
except ValueError:
    logger.warning(warning_msg.format("CHUNK_SIZE", CHUNK_SIZE))
    
# -----------------
try:
    CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", CHUNK_OVERLAP))
except ValueError:
    logger.warning(warning_msg.format("CHUNK_OVERLAP", CHUNK_OVERLAP))
   

# If errors were detected, kill the process:
if errors:
    logger.critical(f"Errors ({errors}) were detected in your environment setup. Please fix them by looking at '.env.template'.")
    sys.exit()
