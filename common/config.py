import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    # Providing defaults here prevents 'None' values and makes local dev easier
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "app_db")
    
    # Infrastructure Control
    # 'true' / 'false' handling via string comparison
    KEEP_INFRA = os.getenv("KEEP_INFRA", "false").lower() == "true"
    
    # Worker Configuration
    POLLING_INTERVAL = int(os.getenv("WORKER_POLLING_INTERVAL", "60"))
    WORKER_MAX_THREADS = int(os.getenv("WORKER_THREADS", "5"))
    
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "user")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "password")
    EMAIL_TO = os.getenv("ALERT_RECIPIENT", "email")