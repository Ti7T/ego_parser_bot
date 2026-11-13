import discord
from discord.ext import commands
from discord import app_commands

from localization import t


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Показать список доступных команд / Show available commands",
    )
    async def help(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        is_admin = (
            interaction.guild is not None
            and interaction.user.guild_permissions.manage_guild
        )

        container = discord.ui.Container()
        container.add_item(discord.ui.TextDisplay(
            f"{t(user_id, 'help_title')}\n"
            f"{t(user_id, 'help_subtitle')}\n\n"
            f"{t(user_id, 'help_intro')}"
        ))
        container.add_item(discord.ui.Separator(
            spacing=discord.SeparatorSpacing.large
        ))
        container.add_item(discord.ui.TextDisplay(t(user_id, "help_stats")))
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(t(user_id, "help_account")))

        if is_admin:
            container.add_item(discord.ui.Separator(
                spacing=discord.SeparatorSpacing.large
            ))
            container.add_item(discord.ui.TextDisplay(t(user_id, "help_roles")))
            container.add_item(discord.ui.Separator())
            container.add_item(discord.ui.TextDisplay(t(user_id, "help_limits")))
            container.add_item(discord.ui.Separator())
            container.add_item(discord.ui.TextDisplay(t(user_id, "help_admin")))

        container.add_item(discord.ui.Separator(
            spacing=discord.SeparatorSpacing.large
        ))
        container.add_item(discord.ui.TextDisplay(t(user_id, "help_footer")))

        view = discord.ui.LayoutView()
        view.add_item(container)
        await interaction.response.send_message(view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
