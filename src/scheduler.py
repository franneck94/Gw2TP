import datetime
from typing import Any

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from .db import AristocracyRelic
from .db import DragonHunterRune
from .db import FireworksRelic
from .db import GuardianRune
from .db import ScholarRune
from .db import SessionLocal
from .db import ThiefRelic
from .db import cleanup_old_records
from .helper import host_url
from .helper import is_running_on_railway


api_base = host_url()


async def _fetch_single_request(
    db: Session,
    api_command: str,
    data_keys: list[str],
    data_cls: type,
) -> None:
    async with aiohttp.ClientSession() as session:  # noqa: SIM117
        async with session.get(f"{api_base}{api_command}") as response:
            data: dict[str, Any] = await response.json()
            if data.get("detail", "") == "Not Found":
                print(f"API command '{api_command}' not found.")
                return
            kwargs = {}

            for data_key in data_keys:
                kwargs.update(
                    {
                        key: value
                        for key, value in data.items()
                        if key.startswith(data_key)
                    }
                )

            db.add(
                data_cls(
                    **kwargs,
                    timestamp=datetime.datetime.now(
                        tz=datetime.timezone(datetime.timedelta(hours=2), "UTC")
                    ),
                )
            )
            db.commit()


async def fetch_api_data() -> None:
    print("Fetching data...")
    fetch_keys = ["crafting_cost", "sell"]
    db = SessionLocal()
    requests = [
        ("scholar_rune", ScholarRune),
        ("guardian_rune", GuardianRune),
        ("dragonhunter_rune", DragonHunterRune),
        ("relic_of_fireworks", FireworksRelic),
        ("relic_of_thief", ThiefRelic),
        ("relic_of_aristocracy", AristocracyRelic),
    ]
    for request, cls in requests:
        await _fetch_single_request(
            db,
            request,
            fetch_keys,
            cls,
        )
    db.close()
    print("Fetching done...")


def start_scheduler() -> None:
    scheduler = AsyncIOScheduler()

    async def fetch_job() -> None:
        await fetch_api_data()

    def cleanup_job() -> None:
        cleanup_old_records(days=14)
        print("Database cleanup completed...")

    if is_running_on_railway():
        scheduler.add_job(
            fetch_job,
            "interval",
            minutes=15,
            max_instances=1,
        )
        scheduler.add_job(
            cleanup_job,
            "cron",
            hour=0,  # daily at midnight UTC
            minute=0,
            max_instances=1,
        )
    else:
        scheduler.add_job(
            fetch_job,
            "interval",
            seconds=10,
            max_instances=1,
        )
        scheduler.add_job(
            cleanup_job,
            "interval",
            hours=1,
            max_instances=1,
        )
    scheduler.start()
