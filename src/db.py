import datetime
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker


FILE_DIR = Path(__file__).parent
DEFAULT_DB_PATH = FILE_DIR / ".." / "database" / "data.db"
DATABASE_PATH = Path(os.getenv("DATABASE_URL", str(DEFAULT_DB_PATH)))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=db)
Base = declarative_base()


class ItemBase:
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    @property
    def formatted_timestamp(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M")

    def __repr__(self) -> str:
        raise NotImplementedError


class ScholarRune(ItemBase, Base):  # type: ignore
    __tablename__ = "scholar_rune"

    crafting_cost_g: Mapped[int]
    crafting_cost_s: Mapped[int]
    crafting_cost_c: Mapped[int]
    sell_g: Mapped[int]
    sell_s: Mapped[int]
    sell_c: Mapped[int]

    def __repr__(self) -> str:
        return (
            f"<ScholarRune("
            f"id={self.id}, "
            f"sell_g={self.sell_g}, "
            f"sell_s={self.sell_s}, "
            f"sell_c={self.sell_c}, "
            f"crafting_cost_g={self.crafting_cost_g}, "
            f"crafting_cost_s={self.crafting_cost_s}, "
            f"crafting_cost_c={self.crafting_cost_c}, "
            f"timestamp={self.formatted_timestamp})>"
        )


DB_CLASSES = [ScholarRune]


def get_db_data(table_name: str) -> list[ScholarRune]:
    db = SessionLocal()
    for db_class in DB_CLASSES:
        if db_class.__tablename__ == table_name:
            data = db.query(db_class).all()
            db.close()
            return data
    return []


Base.metadata.create_all(bind=db)
