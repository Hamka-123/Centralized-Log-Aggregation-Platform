import logging
from common.logging_setup import setup_logging

from common.config import Config
from src.db_sync import get_db_connection

from src.repositories.data_fetcher import DataFetcher
from src.utils.smtp_client import SMTPClient
from src.services.alert_engine import AlertEngine
from src.workers.worker_controller import WorkerController

# Initialize centralized logging for the Worker service
setup_logging("worker")
logger = logging.getLogger(__name__)

def main():
    # 1. Prepare configuration from shared module
    config = Config()
    logger.info(f"Attempting to connect to DB at {config.DB_HOST}:{config.DB_PORT}")

    smtp_config = {
        'SERVER': config.SMTP_SERVER,
        'PORT': config.SMTP_PORT,
        'USER': config.SMTP_USER,
        'PASSWORD': config.SMTP_PASSWORD,
        'RECIPIENT': config.EMAIL_TO
    }
    
    # 2. Dependency Injection
    fetcher = DataFetcher(get_db_connection)
    mailer = SMTPClient(smtp_config)
    engine = AlertEngine(fetcher, mailer)
    
    # 3. Start (graceful shutdown is handled inside WorkerController via signal handlers)
    controller = WorkerController(engine, config)
    controller.start()

if __name__ == "__main__":
    main()
