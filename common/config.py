import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME")
    DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    
    # Infrastructure Control for tests
    KEEP_INFRA = os.getenv("KEEP_INFRA", "false").lower() == "true"
    # Added explicit boolean conversion for SMTP disabling
    DISABLE_SMTP = os.getenv("DISABLE_SMTP", "false").lower() == "true"
    
    # Worker Configuration
    POLLING_INTERVAL = int(os.getenv("WORKER_POLLING_INTERVAL", "60"))
    WORKER_MAX_THREADS = int(os.getenv("WORKER_THREADS", "5"))
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "user")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "password")
    EMAIL_TO = os.getenv("ALERT_RECIPIENT", "email")
    
    # Logging configuration
    LOG_DIR = os.getenv("LOG_DIR", "./logs")
    # Safer conversion to int without eval()
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "5242880"))
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "3"))