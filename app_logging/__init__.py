# app_logging/__init__.py

import logging
import sys

def setup_logging():
    logger = logging.getLogger('my_application')  # Use your application's name
    logger.setLevel(logging.INFO)  # Or whatever level you want

    # Create a handler that writes log messages to sys.stderr
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.INFO)  # Or whatever level you want

    # Create a formatter that includes timestamp and log level
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the handler
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    # Check if the handler is already added to avoid duplicates
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        logger.addHandler(stream_handler)

# Now, you can call this function from your main module
