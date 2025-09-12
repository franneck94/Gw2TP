import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column


Base = declarative_base()


class ItemBase:
    __tablename__: str

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.datetime.now(
            tz=datetime.timezone(datetime.timedelta(hours=2), "UTC")
        ),
    )

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
            f"timestamp={self.timestamp})>"
        )


class ScholarRune(ItemBase, Base):  # type: ignore
    __tablename__ = "scholar_rune"


class GuardianRune(ItemBase, Base):  # type: ignore
    __tablename__ = "guardian_rune"


class DragonHunterRune(ItemBase, Base):  # type: ignore
    __tablename__ = "dragonhunter_rune"


class FireworksRelic(ItemBase, Base):  # type: ignore
    __tablename__ = "relic_of_fireworks"


class ThiefRelic(ItemBase, Base):  # type: ignore
    __tablename__ = "relic_of_thief"


class AristocracyRelic(ItemBase, Base):  # type: ignore
    __tablename__ = "relic_of_aristocracy"


DB_CLASSES: list[ItemBase] = [
    ScholarRune,
    GuardianRune,
    DragonHunterRune,
    FireworksRelic,
    ThiefRelic,
    AristocracyRelic,
]


def cleanup_old_records(
    db: Session,
    days: int = 14,
) -> None:
    cutoff_date = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) - datetime.timedelta(days=days)
    try:
        for db_class in DB_CLASSES:
            db.query(db_class).filter(db_class.timestamp < cutoff_date).delete()
        db.commit()
    finally:
        db.close()


def get_db_data(
    db: Session,
    table_name: str,
    start_datetime: datetime.datetime | None = None,
    end_datetime: datetime.datetime | None = None,
) -> list[ItemBase]:
    try:
        for db_class in DB_CLASSES:
            if db_class.__tablename__ == table_name:
                if start_datetime and end_datetime:
                    return (
                        db.query(db_class)
                        .filter(db_class.timestamp >= start_datetime)
                        .filter(db_class.timestamp <= end_datetime)
                        .all()
                    )
                if start_datetime:
                    return (
                        db.query(db_class)
                        .filter(db_class.timestamp >= start_datetime)
                        .all()
                    )
                if end_datetime:
                    return (
                        db.query(db_class)
                        .filter(db_class.timestamp <= end_datetime)
                        .all()
                    )

                return db.query(db_class).all()
    finally:
        db.close()
    return []
