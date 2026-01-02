import logging
import os

def get_logger(module_name):
    """
    Creates a structured logger that writes to both the console 
    and the 'bot.log' file with timestamps.
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        # Define the log format (Time - Name - Level - Message)
        # This fulfills the assignment's requirement for structured logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 1. File Handler: Writes to 'bot.log' in the project root
        file_handler = logging.FileHandler('bot.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 2. Stream Handler: Also prints to your VS Code terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
