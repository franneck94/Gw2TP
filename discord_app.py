import os
from typing import Any

import aiohttp
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "/gw2tp"
COMMANDS = [
    f"{COMMAND_PREFIX} gear_salvage",
    f"{COMMAND_PREFIX} relic_of_fireworks",
    f"{COMMAND_PREFIX} scholar_rune",
    f"{COMMAND_PREFIX} rare_gear_craft",
    f"{COMMAND_PREFIX} gear_to_ecto",
    f"{COMMAND_PREFIX} get_price [ITEM_ID]",
]


def is_running_on_railway():
    return "RAILWAY_STATIC_URL" in os.environ or "PORT" in os.environ


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


uses_server = is_running_on_railway()
intents = discord.Intents.default()
intents.message_content = True
port = int(os.environ.get("PORT", 8000))
if uses_server:
    api_base = "https://gw2tp-production.up.railway.app/api/"
else:
    api_base = "http://127.0.0.1:8000/api/"
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

COMMANDS_LIST = [
    "gear_salvage",
    "relic_of_fireworks",
    "scholar_rune",
    "rare_gear_craft",
    "gear_to_ecto",
    "get_price",
]

async def gw2tp_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=cmd, value=cmd)
        for cmd in COMMANDS_LIST
        if current.lower() in cmd
    ]

@app_commands.command(name="gw2tp", description="GW2TP commands")
@app_commands.describe(command="Command to run")
@app_commands.autocomplete(command=gw2tp_autocomplete)
async def gw2tp(interaction: discord.Interaction, command: str):
    await interaction.response.send_message(f"Selected command: {command}")


client.tree.add_command(gw2tp)

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
            value=f"🪙 Gold: {g}\n🥈 Silver: {s}\n🥉 Copper: {c}",
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
        help_message = "Available commands:\n" + "\n".join(COMMANDS_LIST)
        await message.channel.send(help_message)
        return

    if message.content.startswith(f"{COMMAND_PREFIX} gear_salvage"):
        title = "Gear Salvage Prices"
        api_url = api_base + "gear_salvage"
    elif message.content.startswith(f"{COMMAND_PREFIX} relic_of_fireworks"):
        title = "Relic of Fireworks"
        api_url = api_base + "relic_of_fireworks"
    elif message.content.startswith(f"{COMMAND_PREFIX} scholar_rune"):
        title = "Scholar Rune"
        api_url = api_base + "scholar_rune"
    elif message.content.startswith(f"{COMMAND_PREFIX} rare_gear_craft"):
        title = "Rare Gear Craft"
        api_url = api_base + "rare_gear_to_ecto"
    elif message.content.startswith(f"{COMMAND_PREFIX} gear_to_ecto"):
        title = "Rare Gear to Ecto"
        api_url = api_base + "gear_to_ecto"
    elif message.content.startswith(f"{COMMAND_PREFIX} get_price"):
        item_id = message.content.split()[2] if len(message.content.split()) > 1 else ""
        title = f"Price for Item ID: {item_id}"
        api_url = api_base + f"price?item_id={item_id}"
    else:
        await message.channel.send("Unknown command. Use `/gw2tp help` for a list of commands.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            data: dict[str, Any] = await resp.json()

    embed = create_price_embed(data, title)
    await message.channel.send(embed=embed)


client.run(TOKEN)
