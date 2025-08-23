import os
from typing import Any

import aiohttp
import discord


TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "/gw2tp"
COMMANDS_LIST = {
    # runes
    "scholar_rune",
    "dragonhunter_rune",
    "guardian_rune",
    # relics
    "relic_of_fireworks",
    "relic_of_aristocracy",
    "relic_of_thief",
    # rare / ecto
    "rare_weapon_craft",
    "rare_gear_salvage",
    "ecto",
    # gear
    "gear_salvage",
    "common_gear_salvage",
    # t5
    "t5_mats_buy",
    "t5_mats_sell",
    # general
    "profits",
    "get_price",
    # forge
    "smybol_enh_forge",
    "loadstone_forge",
}
COMMANDS = [f"{COMMAND_PREFIX} {cmd}" for cmd in COMMANDS_LIST]


def is_running_on_railway():  # noqa: ANN201
    return "RAILWAY_STATIC_URL" in os.environ or "PORT" in os.environ


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
uses_server = is_running_on_railway()
port = int(os.environ.get("PORT", "8000"))
if uses_server:
    api_base = "https://gw2tp-production.up.railway.app/api/"
else:
    api_base = "http://127.0.0.1:8000/api/"


def create_price_embed(
    data: dict[str, float],
    title: str,
) -> discord.Embed:
    embed = discord.Embed(title=title, color=0x1ABC9C)

    keys_list = list(data.keys())
    if len(data) % 3 == 0:
        rows = [key.replace("_g", "") for key in keys_list[::3]]
    else:
        rows = [key.replace("_g", "") for key in keys_list[2::3]]

    for row in rows:
        g = data.get(f"{row}_g", 0)
        s = data.get(f"{row}_s", 0)
        c = data.get(f"{row}_c", 0)
        name = row.replace("_", " ").title()

        embed.add_field(
            name=name,
            value=f"{g} 🪙   {s} ⚪   {c} 🟤",
            inline=False,
        )

    return embed


@client.event
async def on_message(
    message: discord.Message,
) -> None:
    if message.author == client.user:
        return

    if message.content.startswith(f"{COMMAND_PREFIX} help"):
        embed = discord.Embed(
            title="GW2TP Bot Commands",
            color=0x3498DB,
        )
        for cmd in COMMANDS_LIST:
            embed.add_field(
                name="",
                value=f"{COMMAND_PREFIX} {cmd}",
                inline=False,
            )
        await message.channel.send(embed=embed)
        return

    command = message.content
    base_command = command.split()[0] if len(command.split()) > 0 else ""
    sub_command = command.split()[1] if len(command.split()) > 1 else ""

    if command.startswith(f"{COMMAND_PREFIX} ecto"):
        title = "Ecto Price Check"
        api_url = api_base + "price?item_id=19721"
    elif command.startswith(f"{COMMAND_PREFIX} get_price"):
        item_id = (
            command.split()[2]
            if len(command.split()) > 1
            else ""
        )
        title = f"Price for Item ID: {item_id}"
        api_url = api_base + f"price?item_id={item_id}"
    elif base_command == COMMAND_PREFIX and sub_command and COMMANDS_LIST:
        if command.startswith(f"{COMMAND_PREFIX} {sub_command}"):
            title = " ".join([w.upper() for w in sub_command.split("_")])
            api_url = api_base + sub_command
    elif command.startswith(COMMAND_PREFIX):
        await message.channel.send(
            "Unknown command. Use `/gw2tp help` for a list of commands.",
        )
        return
    else:
        return

    async with aiohttp.ClientSession() as session:  # noqa: SIM117
        async with session.get(api_url) as resp:
            data: dict[str, Any] = await resp.json()

    embed = create_price_embed(data, title)
    await message.channel.send(embed=embed)


client.run(TOKEN)
