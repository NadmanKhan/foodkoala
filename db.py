from typing import Optional
from sqlmodel import create_engine, text
from sqlalchemy.engine import Engine

from . import models
from . import settings

# Database engine is created only once (a singleton)
_engine: Optional[Engine] = None

def engine() -> Engine:
    global _engine
    if _engine is None:
        connect_args = {"check_same_thread": False}
        _engine = create_engine(
            settings.DATABASE_URL,
            echo=(settings.ENVIRONMENT == settings.EnvType.DEVELOPMENT),
            connect_args=connect_args,
        )
        if _engine.url.get_backend_name() == "sqlite":
            with _engine.connect() as connection:
                connection.execute(text("PRAGMA foreign_keys=ON"))
        models.SQLModel.metadata.create_all(_engine)
    return _engine
