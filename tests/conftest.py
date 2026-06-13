import docker
import pytest
import subprocess
import time
import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from the .env file in the project root
load_dotenv()

@pytest.fixture(scope="session")
def docker_client():
    """
    Create and return a Docker client for tests.
    """
    return docker.from_env()

@pytest.fixture(scope="session", autouse=True)
def setup_infrastructure():
    """
    Fixture to manage the lifecycle of Docker containers.
    Starts the infrastructure before tests and stops it after.
    """
    print("\n--- Starting Docker Compose ---")
    # Launch containers
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    
    # Wait for API readiness (Health Check)
    api_url = "http://localhost:8000/health"
    max_attempts = 15
    for attempt in range(max_attempts):
        try:
            response = requests.get(api_url, timeout=2)
            if response.status_code == 200:
                print("\n--- API is ready ---")
                break
        except requests.exceptions.ConnectionError:
            print(f"Waiting for API... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(2)
    else:
        # If the loop finishes without break, the API did not start
        subprocess.run(["docker", "compose", "down"], check=True)
        pytest.fail("API did not respond within the allocated time (30 seconds). Tests stopped.")
        
    yield  # --- All tests are executed here ---
    
    # Check if we should keep the infrastructure running
    # You can run tests with: KEEP_INFRA=true ./scripts/check_infra.sh
    if os.getenv("KEEP_INFRA", "false").lower() == "true":
        print("\n--- KEEP_INFRA is set to true. Skipping teardown. ---")
    else:
        print("\n--- Stopping Docker Compose ---")
        subprocess.run(["docker", "compose", "down"], check=True)

@pytest.fixture(scope="session")
def db_session():
    """
    Fixture to create a session connection to the real MariaDB database.
    """
    # Get settings from .env
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_name = os.getenv("DB_NAME", "logs_db")
    db_port = os.getenv("DB_PORT", "3306")
    db_host = "localhost"

    # Form the connection string for MariaDB (via pymysql driver)
    database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Create database engine
    engine = create_engine(database_url)
    TestingSessionLocal = sessionmaker(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    yield session  # Pass session to tests
    
    # Close connection after all tests are finished
    session.close()