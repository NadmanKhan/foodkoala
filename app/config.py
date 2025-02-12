from enum import Enum
from dotenv import load_dotenv
import os


class RunMode(str, Enum):
    DEV = "dev"
    PROD = "prod"


load_dotenv()

RUN_MODE = os.getenv("RUN_MODE", RunMode.DEV)
API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
API_RESOURCE_QUERY_PAGE_MAX = int(os.getenv("API_V1_RESOURCE_MAX_LIMIT", 100))
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


JWT_SECRET = os.getenv("JWT_SECRET", "my_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SESSION_EXPIRE_MINUTES = int(os.getenv("SESSION_EXPIRE", 3600))

PROXIMITY_THRESHOLD = float(os.getenv("PROXIMITY_THRESHOLD", 5000))
