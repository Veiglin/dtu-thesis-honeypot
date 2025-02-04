import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create a logger with the name 'honeypot'
    logger = logging.getLogger('honeypot-logger')
    logger.setLevel(logging.DEBUG)  # Capture all levels of log messages

    # Define a formatter that includes the timestamp, logger name, log level, and message.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Console shows all debug messages and above
    console_handler.setFormatter(formatter)
    
    # --- File Handler ---
    # Ensure the logs directory exists
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set up a RotatingFileHandler: max file size of 10MB, with up to 5 backup files
    file_handler = RotatingFileHandler(os.path.join(log_dir, 'honeypot.log'),
                                       maxBytes=10*1024*1024,
                                       backupCount=5)
    file_handler.setLevel(logging.INFO)  # File logs start from INFO level
    file_handler.setFormatter(formatter)
    
    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
