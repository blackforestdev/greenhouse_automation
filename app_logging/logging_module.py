# logging/logging_module.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_level=logging.INFO, log_file='application.log'):
    # Set up basic logging
    logging.basicConfig(filename=log_file, level=log_level,
                        format='%(asctime)s %(levelname)s: %(message)s '
                               '[in %(pathname)s:%(lineno)d]')
    
    # Optional: Add a rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(log_level)

    return file_handler
