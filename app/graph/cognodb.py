import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase, exceptions

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

class CognoDBManager:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            uri = os.getenv('COGNODB_URI')
            user = os.getenv('COGNODB_USERNAME', 'cognodb')
            password = os.getenv('COGNODB_PASSWORD')

            if not uri or not password:
                print("Missing COGNODB_URI or COGNODB_PASSWORD in environment.")
                return None

            try:
                cls._driver = GraphDatabase.driver(uri, auth=(user, password))
                cls._driver.verify_connectivity()
            except exceptions.DriverError as e:
                print(f"Driver connection failed: {e}")
                cls._driver = None
            except Exception as e:
                print(f"Connection failed: {e}")
                cls._driver = None

        return cls._driver

    @classmethod
    def close(cls):
        if cls._driver:
            cls._driver.close()
            cls._driver = None