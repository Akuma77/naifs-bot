import os, asyncio
from dotenv import load_dotenv
load_dotenv()
import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Naifs Bot logged in as {bot.user}")
    # cogs-ийг ачаална
    await bot.load_extension("cogs.helpcenter")
    await bot.load_extension("cogs.games_and_economy")
    print("Cogs loaded.")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("BOT_TOKEN not found in .env")
    asyncio.run(bot.start(token))
