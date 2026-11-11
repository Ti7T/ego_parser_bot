import discord
from discord.ext import commands
from discord import app_commands

from localization import LANGUAGES, get_language, set_language, t


class LanguageView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                t(interaction.user.id, "language_only_owner"),
                ephemeral=True,
            )
            return False
        return True

    async def choose(self, interaction: discord.Interaction, language: str) -> None:
        if get_language(interaction.user.id) == language:
            await interaction.response.send_message(
                t(interaction.user.id, "language_same"),
                ephemeral=True,
            )
            return

        set_language(interaction.user.id, language)
        await interaction.response.edit_message(
            content=(
                f"{t(interaction.user.id, 'language_title')}\n"
                f"{t(interaction.user.id, 'language_saved', language=LANGUAGES[language])}"
            ),
            view=self,
        )

    @discord.ui.button(label="🇷🇺 Русский", style=discord.ButtonStyle.secondary)
    async def russian(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose(interaction, "ru")

    @discord.ui.button(label="🇬🇧 English", style=discord.ButtonStyle.secondary)
    async def english(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose(interaction, "en")


class LanguageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="language",
        description="Изменить язык ответов бота / Change the bot language",
    )
    async def language(self, interaction: discord.Interaction):
        language = get_language(interaction.user.id)
        await interaction.response.send_message(
            f"{t(interaction.user.id, 'language_title')}\n"
            f"{t(interaction.user.id, 'language_description')}\n"
            f"{t(interaction.user.id, 'language_current', language=LANGUAGES[language])}",
            view=LanguageView(interaction.user.id),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(LanguageCog(bot))
