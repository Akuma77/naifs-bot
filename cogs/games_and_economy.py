import random
import time
from discord.ext import commands
from db import (
    get_user,
    create_user,
    update_balance,
    get_balance,
    update_exp,
    get_level,
    update_last_action,
    seconds_left,
)

# --- CONFIG ---
NON_THEFT_COOLDOWN = 5            # бүх command (slot/roulette/send...) 5sec cooldown
ROBBERY_WALLET_COOLDOWN = 12*3600 # 12 цаг
ROBBERY_BANK_COOLDOWN = 24*3600   # 24 цаг

MIN_SLOT = 100
MAX_SLOT = 10000
MIN_ROUL = 300
MAX_ROUL = 20000

class GamesEconomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------
    # GLOBAL 5 SEC COOLDOWN (non-theft)
    # ------------------------------------------------------
    def check_non_theft_cd(self, u):
        left = seconds_left(u.get("last_action"), NON_THEFT_COOLDOWN)
        return left

    async def try_use_action(self, ctx):
        user = get_user(str(ctx.author.id))
        if not user:
            await ctx.reply("⚠️ Та бүртгэлгүй байна. `/register` гэж бичээрэй.")
            return False
        left = self.check_non_theft_cd(user)
        if left > 0:
            await ctx.reply(f"⏳ Та саяхан команд ашигласан байна. {left} секунд хүлээнэ үү.")
            return False
        update_last_action(str(ctx.author.id), "last_action")
        return True

    # ------------------------------------------------------
    # REGISTER
    # ------------------------------------------------------
    @commands.hybrid_command(name="register", description="Наifs ID үүсгэх")
    async def register(self, ctx):
        ok = create_user(str(ctx.author.id))
        if ok:
            await ctx.reply("🎉 **Шинэ ID үүсгэгдлээ!** Та 5000 moonstone (ms) авлаа.", ephemeral=True)
        else:
            await ctx.reply("⚠️ Та аль хэдийн бүртгэлтэй байна.", ephemeral=True)

    # ------------------------------------------------------
    # PROFILE
    # ------------------------------------------------------
    @commands.hybrid_command(name="profile", description="Таны профайл харах")
    async def profile(self, ctx):
        u = get_user(str(ctx.author.id))
        if not u:
            await ctx.reply("⚠️ Та бүртгэлгүй байна.")
            return
        level = get_level(str(ctx.author.id))
        bal = get_balance(str(ctx.author.id))
        await ctx.reply(
            f"📜 **Таны профайл**\n"
            f"⭐ Level: `{level}`\n"
