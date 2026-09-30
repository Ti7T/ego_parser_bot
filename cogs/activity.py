import discord
from discord.ext import commands
from discord import app_commands
from services import get_player, create_activity_graphs
from typing import Optional
from database import get_linked_player

class ActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="activity",
        description="Показать активность игрока на EGO серверах"
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
        image = await create_activity_graphs(player)
        file = discord.File(
            fp=image, 
            filename="actvity.png"
        )
        await interaction.followup.send(file=file)

async def setup(bot):
    await bot.add_cog(ActivityCog(bot))