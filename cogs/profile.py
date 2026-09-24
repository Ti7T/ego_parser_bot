import discord
from discord.ext import commands
from discord import app_commands
from services import create_profile, get_player
from typing import Optional
from database import get_linked_player

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="Показать статистику игрока на EGO серверах"
    )
    @app_commands.describe(
        nick="Ник игрока на EGO"
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        nick: Optional[str] = None
    ):
        if nick is None:
            nick = get_linked_player(interaction.user.id)
            if nick is None:
                await interaction.response.send_message(
                    "❌ У тебя не привязан игровой ник.\n"
                    "Используй `/link`, чтобы привязать его.",
                    ephemeral=True
                )
                return

        await interaction.response.defer(thinking=True)
        player = await get_player(nick)
        image = await create_profile(player)
        file = discord.File(
            fp=image,
            filename="profile.png"
        )
        await interaction.followup.send(file=file)

    @app_commands.command(
        name="private_profile",
        description="Показать невидимую для остальных кроме вас статистику игрока на EGO серверах"
    )
    @app_commands.describe(
        nick="Ник игрока на EGO"
    )
    async def private_profile(
        self,
        interaction: discord.Interaction,
        nick: Optional[str] = None
    ):
        if nick is None:
            nick = get_linked_player(interaction.user.id)
            if nick is None:
                await interaction.response.send_message(
                    "❌ У тебя не привязан игровой ник.\n"
                    "Используй `/link`, чтобы привязать его.",
                    ephemeral=True
                )
                return

        await interaction.response.defer(ephemeral=True, thinking=True)
        player = await get_player(nick)
        image = await create_profile(player)
        file = discord.File(
            fp=image,
            filename="profile.png"
        )
        await interaction.followup.send(file=file, ephemeral=True)

# Функция "setup" обязательна для загрузки Кога
async def setup(bot):
    await bot.add_cog(ProfileCog(bot))