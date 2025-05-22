import logging
import os
import sys
from .config import AGENT_DIR # Assuming config.py is in the same directory (slide_generate_agent)

LOG_DIR = os.path.join(AGENT_DIR, 'logs')
LOG_FILE_NAME = 'slide_agent.log'  # Central log file name
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# Ensure log directory exists when this module is imported
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(logger_name: str = None):
    """
    Configures and returns a logger instance.
    If logger_name is None, it defaults to the root logger of this setup,
    otherwise, it gets a logger specific to the provided name (e.g., __name__ from the calling module).
    Logs will be output to both console and a central log file.
    """
    if logger_name is None:
        # Use a generic name if none provided, or consider configuring the root logger directly
        # For this setup, let's use a distinct name for the base configuration logger
        # to avoid conflicts if other libraries configure the root logger.
        base_logger_name = 'slide_agent_base_config'
    else:
        base_logger_name = logger_name

    logger = logging.getLogger(base_logger_name)

    # Configure only if no handlers are present, to avoid duplicate handlers on multiple calls
    if not logger.handlers:
        logger.setLevel(logging.INFO)  # Set level on the logger itself
        # Set propagate to False if logger_name is specific, to avoid logs going to a parent
        # logger if the parent (e.g. root) also gets configured by another part of the system.
        # If logger_name is intended to be part of a hierarchy that IS configured, this might be True.
        logger.propagate = False

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
        )

        # StreamHandler for console output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO) # Set level on handler
        logger.addHandler(stream_handler)

        # FileHandler for file output
        file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a') # Append mode
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO) # Set level on handler
        logger.addHandler(file_handler)

    return logger
