import discord
from discord.ext import commands
from discord import app_commands

from localization import get_language
from services import create_profile, get_player
from utils import resolve_nick_argument


class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="Показать статистику игрока на EGO серверах / Show EGO player statistics",
    )
    @app_commands.describe(
        nick="Ник игрока на EGO / EGO player nickname",
        member="Discord-пользователь с привязанным через /link ником / Discord user linked with /link",
    )
    async def profile(
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
        image = await create_profile(player, get_language(interaction.user.id))
        file = discord.File(fp=image, filename="profile.png")
        await interaction.followup.send(file=file)

    @app_commands.command(
        name="private_profile",
        description="Показать приватную статистику игрока / Show a private player profile",
    )
    @app_commands.describe(
        nick="Ник игрока на EGO / EGO player nickname",
        member="Discord-пользователь с привязанным через /link ником / Discord user linked with /link",
    )
    async def private_profile(
        self,
        interaction: discord.Interaction,
        nick: str | None = None,
        member: discord.Member | None = None,
    ):
        nick = await resolve_nick_argument(nick, member, interaction)
        if nick is None:
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        player = await get_player(nick)
        image = await create_profile(player, get_language(interaction.user.id))
        file = discord.File(fp=image, filename="profile.png")
        await interaction.followup.send(file=file, ephemeral=True)


async def setup(bot):
    await bot.add_cog(ProfileCog(bot))
