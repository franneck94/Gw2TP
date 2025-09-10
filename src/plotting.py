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
    if len(data) == 0:
        return ""

    plt.style.use("dark_background")
    timestamps = [e.timestamp.strftime("%H:%M") for e in data]
    sell_price = [(e.sell_g + e.sell_s / 100 + e.sell_c / 10_000) for e in data]
    crafting_price = [
        (
            e.crafting_cost_g
            + e.crafting_cost_s / 100
            + e.crafting_cost_c / 10_000
        )
        for e in data
    ]
    plt.figure(figsize=(16, 9))
    plt.plot(timestamps, sell_price, marker="o", label="Sell Price")
    plt.plot(timestamps, crafting_price, marker="o", label="Crafting Price")
    plt.axhline(
        y=sum(sell_price) / len(sell_price),
        color="orange",
        linestyle="--",
        label="Mean Sell Price",
    )
    plt.axhline(
        y=sum(crafting_price) / len(crafting_price),
        color="cyan",
        linestyle="--",
        label="Mean Crafting Price",
    )
    plt.plot(timestamps, crafting_price, marker="o", label="Crafting Price")
    plt.gca().get_yaxis().set_major_formatter(
        mpl.ticker.StrMethodFormatter("{x:.3f}")
    )
    plt.xticks(rotation=50)
    plt.title(f"{name} Timestamps")
    plt.ylabel("Price in Gold")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plot = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    return plot
