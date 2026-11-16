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
from localization import TEXTS
import json

class ProgressCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="progress",
        description="Статистика игрока за период / Player statistics over a period",
    )
    @app_commands.describe(
        days="Количество дней для сравнения / Number of days to compare",
        member="Discord-пользователь с привязанным через /link ником / Discord user linked with /link",
    )
    async def progress(
        self,
        interaction: discord.Interaction,
        days: app_commands.Range[int, 1, 365] = 1,
        member: discord.Member | None = None,
    ):
        language = get_language(interaction.user.id)
        labels = TEXTS.get(language, TEXTS["ru"])

        nick = await resolve_nick_argument(
            nick=None,
            member=member,
            interaction=interaction,
        )
        if nick is None:
            return

        await interaction.response.defer(thinking=True)

        today = datetime.now(ZoneInfo("Europe/Moscow")).date()

        previous_date = (today - timedelta(days=days * 3)).isoformat()
        middle_date = (today - timedelta(days=days * 2)).isoformat()
        current_date = (today - timedelta(days=days)).isoformat()

        previous_snapshot = get_snapshot(nick, previous_date)
        middle_snapshot = get_snapshot(nick, middle_date)
        current_snapshot = get_snapshot(nick, current_date)

        if not previous_snapshot or not middle_snapshot or not current_snapshot:
            await interaction.followup.send(
                labels["progress_snapshot_not_found"].format(
                    previous_date=previous_date,
                    middle_date=middle_date,
                    current_date=current_date
                )
            )
            return

        previous_player = JSONConverter.from_snapshot(
            json.loads(previous_snapshot)
        )
        middle_player = JSONConverter.from_snapshot(
            json.loads(middle_snapshot)
        )
        current_player = JSONConverter.from_snapshot(
            json.loads(current_snapshot)
        )

        image = await create_progress_card(
            previous_player,
            middle_player,
            current_player,
            days,
            language,
        )

        file = discord.File(fp=image, filename="progress.png")
        await interaction.followup.send(file=file)


async def setup(bot):
    await bot.add_cog(ProgressCog(bot))
