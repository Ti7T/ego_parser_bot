import discord
from discord.ext import commands
from discord import app_commands

from database import set_linked_player, remove_linked_player
from localization import t


class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="link",
        description="Привязать свой игровой ник к Discord / Link your in-game nickname",
    )
    @app_commands.describe(nick="Твой ник на EGO / Your EGO nickname")
    async def link(self, interaction: discord.Interaction, nick: str):
        set_linked_player(interaction.user.id, nick)
        await interaction.response.send_message(
            t(interaction.user.id, "link_success", nick=nick),
            ephemeral=True,
        )

    @app_commands.command(
        name="unlink",
        description="Отвязать игровой ник от Discord / Unlink your in-game nickname",
    )
    async def unlink(self, interaction: discord.Interaction):
        remove_linked_player(interaction.user.id)
        await interaction.response.send_message(
            t(interaction.user.id, "unlink_success"),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(LinkCog(bot))
