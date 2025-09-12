import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gw2tp.db_schema import Base


FILE_DIR = Path(__file__).parent
DEFAULT_DB_PATH = FILE_DIR / ".." / "database" / "data.db"
DATABASE_PATH = Path(os.getenv("DATABASE_URL", str(DEFAULT_DB_PATH)))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=db)
Base.metadata.create_all(bind=db)
