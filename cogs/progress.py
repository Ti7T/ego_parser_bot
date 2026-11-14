import discord
from discord.ext import commands
from discord import app_commands
from localization import get_language
from services import create_progress_card, get_player
from utils import resolve_nick_argument
from database import get_snapshot
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from api import JSONConverter
from config import BASE_URL
import json

class ProgressCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="progress",
        description="Показать статистику игрока на EGO серверах / Show EGO player statistics",
    )
    @app_commands.describe(
        days="Ник игрока на EGO / EGO player nickname",
        member="Discord-пользователь с привязанным через /link ником / Discord user linked with /link",
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        days: app_commands.Range[int, 1, 365] = 1,
        member: discord.Member | None = None
    ):
        nick = await resolve_nick_argument(nick=None, member=member, interaction=interaction)
        if nick is None:
            return

        target_date = (
            datetime.now(ZoneInfo("Europe/Moscow"))
            - timedelta(days=days)
        ).date()

        await interaction.response.defer(thinking=True)
        current_player = await get_player(nick)
        previous_player_str = get_snapshot(nick, target_date)
        if not previous_player_str:
            await interaction.followup.send("error")
        previous_player_json = json.loads(previous_player_str)
        previous_player = JSONConverter.from_snapshot(previous_player_json)
        image = await create_progress_card(previous_player, current_player, days, get_language(interaction.user.id))
        file = discord.File(fp=image, filename="profile.png")
        await interaction.followup.send(file=file)


async def setup(bot):
    await bot.add_cog(ProgressCog(bot))
