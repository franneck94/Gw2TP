import base64
import datetime
import io
from typing import Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt

from .db import ItemBase


mpl.use("Agg")


def get_date_plot(
    data: Sequence[ItemBase],
    name: str,
) -> str:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    last_24hrs = now - datetime.timedelta(minutes=10)
    filtered_data = [e for e in data if e.timestamp >= last_24hrs]
    timestamps = [e.timestamp.strftime("%H:%M") for e in filtered_data]
    sell_price = [e.sell for e in filtered_data]
    plt.figure(figsize=(16, 9))
    plt.plot(timestamps, sell_price, marker="o")
    plt.xticks(rotation=50)
    plt.title(f"{name} Timestamps")
    plt.xlabel("Timestamp")
    plt.ylabel("Sell Price")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    ecto_plot = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    return ecto_plot
