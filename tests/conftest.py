import docker
import pytest
import subprocess
import time
import requests
import os
import pymysql 
from dotenv import load_dotenv

load_dotenv()

# Создает объект клиента Docker, который позволяет управлять контейнерами прямо из кода тестов (через библиотеку docker-py).
@pytest.fixture(scope="session")
def docker_client():
    return docker.from_env()

# Setup-фикстура
@pytest.fixture(scope="session", autouse=True)
def setup_infrastructure():
    # ... (код запуска инфраструктуры можно оставить без изменений) ...
    keep_infra = os.getenv("KEEP_INFRA", "false").lower() == "true"
    if keep_infra:
        print("\n--- KEEP_INFRA=true detected. Skipping startup. ---")
    else:
        print("\n--- Starting Docker Compose ---")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
    
    yield
    if not keep_infra:
        subprocess.run(["docker", "compose", "down"], check=True)

# фикстура подключения к бд
@pytest.fixture(scope="session")
def db_connection():
    """
    Создает чистое соединение с базой через pymysql.
    """
    conn = pymysql.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", "3306")),
        autocommit=True # Сразу коммитит изменения
    )
    yield conn
    conn.close()

# Фикстура для наполнения данными
@pytest.fixture(scope="session", autouse=True)
def seed_test_data(db_connection):
    service_name = "test-service"
    
    with db_connection.cursor() as cursor:
        # Проверяем, существует ли сервис
        cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()

        if not result:
            print(f"\n--- Seeding test service: {service_name} ---")
            cursor.execute(
                "INSERT INTO services (service_name, description) VALUES (%s, %s)",
                (service_name, "Integration test service")
            )
    yield

# Фикстура получения ID сервиса
@pytest.fixture(scope="session")
def test_service_id(db_connection):
    service_name = "test-service"
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
            
        # Если не нашли, создаем
        cursor.execute(
            "INSERT INTO services (service_name, description) VALUES (%s, %s)",
            (service_name, "Created by test fixture")
        )
        cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()
        return result[0]