import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"✅ Naifs Bot logged in as {bot.user}")
    # Сlash командуудыг Discord-т бүртгэнэ
    await bot.tree.sync()
    print("🔄 Slash commands synced!")
    print("Cogs loaded.")

async def load_all_extensions():
    await bot.load_extension("cogs.games_and_economy")

async def main():
    await load_all_extensions()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("❌ BOT_TOKEN not found in .env")

    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
