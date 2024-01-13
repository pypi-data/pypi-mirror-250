import os
from dotenv import load_dotenv

load_dotenv()


def run() -> None:
    environment = os.environ.get("ENVIRONMENT", "development")

    print("environment", environment)
