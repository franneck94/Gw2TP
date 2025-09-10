import asyncio
import datetime
from typing import Any

import aiohttp
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from .db import AristocracyRelic
from .db import DragonHunterRune
from .db import FireworksRelic
from .db import GuardianRune
from .db import RareWeaponCraft
from .db import ScholarRune
from .db import SessionLocal
from .db import ThiefRelic
from .helper import host_url


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
                    timestamp=datetime.datetime.now(),  # noqa: DTZ005
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
        ("rare_weapon_craft", RareWeaponCraft),
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
    scheduler = BackgroundScheduler()

    def job() -> None:
        asyncio.run(fetch_api_data())

    scheduler.add_job(
        job,
        "interval",
        seconds=10,
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
