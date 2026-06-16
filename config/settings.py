from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "logs_db"

    # SMTP (для алертов)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your_email@example.com"
    SMTP_PASSWORD: str = "your_password"

    class Config:
        env_file = ".env" # Автоматически читает твой файл .env

settings = Settings()