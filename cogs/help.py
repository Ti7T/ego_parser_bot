import discord
from discord.ext import commands
from discord import app_commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Показать список доступных команд"
    )
    async def help(self, interaction: discord.Interaction):
        is_admin = (
            interaction.guild is not None
            and interaction.user.guild_permissions.manage_guild
        )

        container = discord.ui.Container()

        container.add_item(
            discord.ui.TextDisplay(
                "# 📖 EGO Bot\n"
                "Справочник доступных команд\n\n"
                "Получение статистики игроков на EGO "
                "и управление возможностями сервера."
            )
        )

        container.add_item(
            discord.ui.Separator(
                spacing=discord.SeparatorSpacing.large
            )
        )

        container.add_item(
            discord.ui.TextDisplay(
                "## 📊 Статистика игроков\n"
                "`/profile [nick]` — профиль игрока.\n"
                "`/private_profile [nick]` — приватный профиль.\n"
                "`/activity [nick]` — графики активности.\n"
                "`/recent_finishes [nick]` — последняя активность."
            )
        )

        container.add_item(
            discord.ui.Separator()
        )

        container.add_item(
            discord.ui.TextDisplay(
                "## 🔗 Аккаунт\n"
                "`/link nick` — привязать игровой ник.\n"
                "`/unlink` — отвязать игровой ник.\n\n"
                "Если `nick` не указан в команде статистики, "
                "используется привязанный аккаунт."
            )
        )

        if is_admin:
            container.add_item(
                discord.ui.Separator(
                    spacing=discord.SeparatorSpacing.large
                )
            )

            container.add_item(
                discord.ui.TextDisplay(
                    "## 🎭 Роли по реакциям\n"
                    "`/reaction_roles_create` — создать сообщение "
                    "для выдачи ролей.\n"
                    "`/reaction_roles_add` — привязать реакцию к роли.\n"
                    "`/reaction_roles_remove` — удалить привязку.\n"
                    "`/reaction_roles_remove_all` — удалить все "
                    "привязки сообщения."
                )
            )

            container.add_item(
                discord.ui.Separator()
            )

            container.add_item(
                discord.ui.TextDisplay(
                    "## ⚙️ Ограничение реакций\n"
                    "`/emoji_limit` — установить лимит реакций.\n"
                    "`/emoji_limit_remove` — убрать лимит.\n"
                    "`/emoji_allow_user` — добавить пользователя "
                    "в исключения.\n"
                    "`/emoji_unallow_user` — убрать пользователя "
                    "из исключений.\n"
                    "`/emoji_allow_role` — добавить роль в исключения.\n"
                    "`/emoji_unallow_role` — убрать роль "
                    "из исключений."
                )
            )

            container.add_item(
                discord.ui.Separator()
            )

            container.add_item(
                discord.ui.TextDisplay(
                    "-# 🔐 Административные команды доступны "
                    "пользователям с правом «Управление сервером»."
                )
            )

        container.add_item(
            discord.ui.Separator(
                spacing=discord.SeparatorSpacing.large
            )
        )

        container.add_item(
            discord.ui.TextDisplay(
                "-# EGO Bot • Справка по командам"
            )
        )

        view = discord.ui.LayoutView()
        view.add_item(container)

        await interaction.response.send_message(
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
