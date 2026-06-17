import logging
import os
from logging.handlers import RotatingFileHandler
from common.config import Config # Import the centralized config

def setup_logging(service_name, log_dir=Config.LOG_DIR):
    # Create the logs directory if it does not exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Use the service name to create a unique log file name (e.g., api.log, worker.log)
    log_file = f"{service_name}.log"

    log_path = os.path.join(log_dir, log_file)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configuration for the file using values from Config
    file_handler = RotatingFileHandler(
        log_path, 
        maxBytes=Config.LOG_MAX_BYTES, 
        backupCount=Config.LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)

    # Configuration for the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)