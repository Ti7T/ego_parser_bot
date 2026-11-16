
import discord
from discord.ext import commands
from discord import app_commands

from database import set_command_channel, get_command_channel, remove_command_channel


class ChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setchannel",
        description="Установить канал для напоминаний бота / Set bot reminder channel",
    )
    @app_commands.describe(
        channel="Канал для напоминаний / Reminder channel"
    )
    @app_commands.default_permissions(administrator=True)
    async def set_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
    ):
        set_command_channel(interaction.guild_id, channel.id)

        await interaction.response.send_message(
            f"Канал для напоминаний установлен: {channel.mention}",
            ephemeral=True,
        )

    @app_commands.command(
        name="getchannel",
        description="Показать канал напоминаний / Show reminder channel",
    )
    @app_commands.default_permissions(administrator=True)
    async def get_channel(self, interaction: discord.Interaction):
        channel_id = get_command_channel(interaction.guild_id)

        if channel_id is None:
            await interaction.response.send_message(
                "Канал для напоминаний не установлен.",
                ephemeral=True,
            )
            return

        channel = interaction.guild.get_channel(channel_id)

        if channel is None:
            await interaction.response.send_message(
                "Сохранённый канал не найден. Установи его заново через /setchannel.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Текущий канал для напоминаний: {channel.mention}",
            ephemeral=True,
        )

    @app_commands.command(
        name="removechannel",
        description="Отключить напоминания / Disable reminders",
    )
    @app_commands.default_permissions(administrator=True)
    async def remove_channel(self, interaction: discord.Interaction):
        remove_command_channel(interaction.guild_id)

        await interaction.response.send_message(
            "Канал для напоминаний отключён.",
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(ChannelCog(bot))
