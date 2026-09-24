import discord
from discord.ext import commands
from discord import app_commands
from database import set_linked_player, remove_linked_player

class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="link",
        description="Привязать свой игровой ник к Discord"
    )
    @app_commands.describe(
        nick="Твой ник на EGO"
    )
    async def link(
        self,
        interaction: discord.Interaction,
        nick: str
    ):
        set_linked_player(interaction.user.id, nick)

        await interaction.response.send_message(
            f"✅ Теперь твой Discord привязан к нику `{nick}`.",
            ephemeral=True
        )

    @app_commands.command(
        name="unlink",
        description="Отвязать игровой ник от Discord"
    )
    async def unlink(
        self,
        interaction: discord.Interaction
    ):
        remove_linked_player(interaction.user.id)

        await interaction.response.send_message(
            "✅ Игровой ник отвязан от твоего Discord.",
            ephemeral=True
        )

    
async def setup(bot):
    await bot.add_cog(LinkCog(bot))