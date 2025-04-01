"""Module for custom loggers. Nice readable logs can save you time when debugging,
do not overlook them. To get a logger, simply use 'get_logger()' and then use
the standard 'debug()', 'info()', etc. methods from that logger.

Inspired by: https://stackoverflow.com/a/56944256 and the standard logging module doc
https://docs.python.org/3/library/logging.html.
"""


import logging
from enum import StrEnum

# -----------------------------------------------------------------------------

class Color(StrEnum):
    """Enumeration of the codes to change the color of text in the loggers/terminal.
    Also contains the 'RESET' code use to prevent leakage of your style to other lines.
    """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    # Use this to prevent your color from affecting more than 1 line:
    RESET = "\x1b[0m"
    
    
class Font(StrEnum):
    """Enumeration of the codes to change the font of text in the loggers/terminal.
    Also contains the 'RESET' code use to prevent leakage of your style to other lines.
    """
    # Basic fonts, supported by most terminals:
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    # Use this to prevent your color from affecting more than 1 line:
    RESET = "\x1b[0m"
    
    
def get_colour_with_font(color : Color, font : Font):
    """Get the code to get both a colour and a font transformation.

    Args:
        color (Color): The color you would like to use.
        font (Font): The font transformation you would like to use.

    Returns:
        str - The combined color and font transformation code.
    """
    font = font.split("[")[1][0:-1]
    color = color.split(";")[1][0:-1]
    return f"\033[{font};{color}m"

# -----------------------------------------------------------------------------

class StandardFormatter(logging.Formatter):
    """A standard formatter for logs."""

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Color.BLUE + format + Color.RESET,
        logging.INFO: Color.WHITE + format + Color.RESET,
        logging.WARNING: Color.YELLOW + format + Color.RESET,
        logging.ERROR: Color.RED + format + Color.RESET,
        logging.CRITICAL: Color.MAGENTA + format + Color.RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# -----------------------------------------------------------------------------

def get_logger(app_name, level = logging.INFO, formatter = StandardFormatter):
    """The main function to get a nicely formatted logger.

    Args:
        app_name (str): The name of the application associated with the logger, enables differientiating
            between various loggers used in parallel by different services for instance.
        level (str, optional): The level of the logger (pls, use standards 'logging.logging_level'). 
            Defaults to logging.INFO.
        formatter (class, optional): The formatter class to instantiate, needs to inherit from
            'logging.Formatter'. Defaults to StandardFormatter.
        
    Returns:
        logging.Logger - A preformatted logger, ready to use.
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(level)

    # Create console handler with a higher log level
    console_handler= logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter())

    logger.addHandler(console_handler)
    
    return logger

