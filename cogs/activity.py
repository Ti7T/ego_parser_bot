import discord
from discord.ext import commands
from discord import app_commands

from localization import get_language
from services import get_player, create_activity_graphs
from utils import resolve_nick_argument


class ActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="activity",
        description="Показать активность игрока / Show player activity",
    )
    @app_commands.describe(
        nick="Ник игрока на EGO / EGO player nickname",
        member="Discord-пользователь с привязанным через /link ником / Discord user linked with /link",
    )
    async def activity(
        self,
        interaction: discord.Interaction,
        nick: str | None = None,
        member: discord.Member | None = None,
    ):
        nick = await resolve_nick_argument(nick, member, interaction)
        if nick is None:
            return

        await interaction.response.defer(thinking=True)
        player = await get_player(nick)
        image = await create_activity_graphs(player, get_language(interaction.user.id))
        file = discord.File(fp=image, filename="activity.png")
        await interaction.followup.send(file=file)


async def setup(bot):
    await bot.add_cog(ActivityCog(bot))
