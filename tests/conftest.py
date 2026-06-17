import docker
import pytest
import subprocess
import time
import requests
import os
import sys
import pymysql 
from dotenv import load_dotenv

load_dotenv()

# Adds the project root to sys.path so tests can import source modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def docker_client():
    """
    Creates a Docker client object that allows you to manage 
    containers directly from your test code (via the docker-py library).
    """
    return docker.from_env()

@pytest.fixture(scope="session", autouse=True)
def setup_infrastructure():
    """
    Setup test-infra fixture
    """
    keep_infra = os.getenv("KEEP_INFRA", "false").lower() == "true"
    if keep_infra:
        print("\n--- KEEP_INFRA=true detected. Skipping startup. ---")
    else:
        print("\n--- Starting Docker Compose ---")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
    
    yield
    if not keep_infra:
        subprocess.run(["docker", "compose", "down"], check=True)

@pytest.fixture(scope="session")
def db_connection():
    """
    Database connection fixture
    Creates a raw connection to the database via pymysql.
    """
    conn = pymysql.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", "3306")),
        autocommit=True 
    )
    yield conn
    conn.close()

@pytest.fixture(scope="session", autouse=True)
def seed_test_data(db_connection):
    """
    Fixture for filling with data
    """
    service_name = "test-service"
    
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()

        if not result:
            print(f"\n--- Seeding test service: {service_name} ---")
            cursor.execute(
                "INSERT INTO services (service_name, description) VALUES (%s, %s)",
                (service_name, "Integration test service")
            )
    yield


@pytest.fixture(scope="session")
def test_service_id(db_connection):
    """
    Fixture for obtaining service ID
    """
    service_name = "test-service"
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
            
        cursor.execute(
            "INSERT INTO services (service_name, description) VALUES (%s, %s)",
            (service_name, "Created by test fixture")
        )
        cursor.execute("SELECT id FROM services WHERE service_name = %s", (service_name,))
        result = cursor.fetchone()
        return result[0]