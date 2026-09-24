import discord
from discord.ext import commands
from discord import app_commands
from services import get_player, create_recent_finishes
from typing import Optional
from database import get_linked_player

class LastActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="last_activity",
        description="Показать последнюю активность игрока на EGO серверах"
    )
    @app_commands.describe(
        nick="Ник игрока на EGO"
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        nick: Optional[str] = None
    ):
        #TODO: нужно сделать отдельную функцию, для проверки ника
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
        image = await create_recent_finishes(player)
        file = discord.File(
            fp=image, 
            filename="recent_finishes.png"
        )
        await interaction.followup.send(file=file)

async def setup(bot):
    await bot.add_cog(LastActivityCog(bot))