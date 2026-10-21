import discord
from discord.ext import commands
from discord import app_commands
from services import get_player, create_recent_finishes
from typing import Optional
from utils import resolve_nick_argument

class RecentFinishesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="recent_finishes",
        description="Показать последнюю активность игрока на EGO серверах"
    )
    @app_commands.describe(
        nick="Ник игрока на EGO"
    )
    async def recent_finishes(
        self,
        interaction: discord.Interaction,
        nick: Optional[str] = None
    ):
        nick = await resolve_nick_argument(nick, interaction) 
        if nick is None:                                                                                        
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
    await bot.add_cog(RecentFinishesCog(bot))