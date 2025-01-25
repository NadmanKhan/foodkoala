from enum import Enum
from dotenv import load_dotenv
import os


class RunMode(str, Enum):
    DEV = "dev"
    PROD = "prod"


load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite://") # "sqlite://" for in-memory database
RUN_MODE = os.getenv("RUN_MODE", RunMode.DEV)
SECRET = os.getenv("SECRET", "my_secret_key")
