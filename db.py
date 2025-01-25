from typing import Optional
from sqlmodel import create_engine, text
from sqlalchemy.engine import Engine

from .models import SQLModel
from .settings import DB_URL, RUN_MODE, RunMode

# Database engine is a singleton
_engine: Optional[Engine] = None


# Function to get the database engine instance
def engine() -> Engine:
    global _engine
    if _engine is None:
        connect_args = {"check_same_thread": False}
        _engine = create_engine(
            DB_URL,
            echo=(RUN_MODE == RunMode.DEV),
            connect_args=connect_args,
        )
        if _engine.url.get_backend_name() == "sqlite":
            with _engine.connect() as connection:
                connection.execute(text("PRAGMA foreign_keys=ON"))
        SQLModel.metadata.create_all(_engine)
    return _engine
