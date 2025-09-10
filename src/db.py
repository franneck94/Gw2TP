import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '../database/data.db')}"

db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=db)
Base = declarative_base()


class ItemBase:
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=datetime.datetime.now(),
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


def get_scholar_history() -> list[ScholarRune]:
    db = SessionLocal()
    history = db.query(ScholarRune).all()
    db.close()
    return history


Base.metadata.create_all(bind=db)
