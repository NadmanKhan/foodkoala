from sqlmodel import Session as DBSession, create_engine
from typing_extensions import Generator

from app.storage.mappers import SQLModel, sqltext
from app.config import DB_URL, RUN_MODE, RunMode

# Database engine is a singleton
_engine = create_engine(
    DB_URL,
    echo=bool(RUN_MODE == RunMode.DEV),
    connect_args={"check_same_thread": False},
)

# Enable foreign key constraints for SQLite
if _engine.url.get_driver_name() == "sqlite":
    with _engine.connect() as connection:
        connection.execute(sqltext("PRAGMA foreign_keys=ON"))

# Drop and create tables
SQLModel.metadata.drop_all(_engine)
SQLModel.metadata.create_all(_engine)


def new_db_session() -> Generator[DBSession, None, None]:
    global _engine
    with DBSession(_engine) as db:
        yield db
