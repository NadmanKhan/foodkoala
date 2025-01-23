from enum import Enum
from dotenv import load_dotenv
import os


class EnvType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://")
ENVIRONMENT = os.getenv("ENVIRONMENT", EnvType.DEVELOPMENT)
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")
