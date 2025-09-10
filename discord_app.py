import os
from typing import Any

import aiohttp
import discord

from src.constants import API
from src.helper import host_url


TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")

COMMANDS = [f"{API.COMMAND_PREFIX} {cmd}" for cmd in API.COMMANDS_LIST]


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
port = int(os.environ.get("PORT", "8000"))
api_base = host_url()


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

    if message.content.startswith(f"{API.COMMAND_PREFIX} help"):
        embed = discord.Embed(
            title="GW2TP Bot Commands",
            color=0x3498DB,
        )
        for cmd in API.COMMANDS_LIST:
            embed.add_field(
                name="",
                value=f"{API.COMMAND_PREFIX} {cmd}",
                inline=False,
            )
        await message.channel.send(embed=embed)
        return

    command = message.content
    base_command = command.split()[0] if len(command.split()) > 0 else ""
    sub_command = command.split()[1] if len(command.split()) > 1 else ""

    if command.startswith(f"{API.COMMAND_PREFIX}"):
        if command.startswith(f"{API.COMMAND_PREFIX} ecto"):
            title = "Ecto Price Check"
            api_url = api_base + "price?item_id=19721"
        elif command.startswith(f"{API.COMMAND_PREFIX} get_price"):
            item_id = command.split()[2] if len(command.split()) > 1 else ""
            title = f"Price for Item ID: {item_id}"
            api_url = api_base + f"price?item_id={item_id}"
        elif base_command == API.COMMAND_PREFIX and sub_command:
            if command.startswith(f"{API.COMMAND_PREFIX} {sub_command}"):
                title = " ".join([w.upper() for w in sub_command.split("_")])
                api_url = api_base + sub_command
            else:
                await message.channel.send(
                    "Unknown command. Use /gw2tp help for a list of commands.",
                )
                return
        elif command.startswith(f"{API.COMMAND_PREFIX}"):
            await message.channel.send(
                "Unknown command. Use /gw2tp help for a list of commands.",
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
