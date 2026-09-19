import discord
from discord.ext import commands
from discord import app_commands

from database import (
    set_emoji_limit,
    get_emoji_limit,
    remove_emoji_limit,

    add_allowed_user,
    remove_allowed_user,
    is_user_allowed,

    add_allowed_role,
    remove_allowed_role,
    is_role_allowed,
)


class EmojiLimiter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================================================
    # Проверка исключения
    # =========================================================

    def is_exempt(self, member: discord.Member) -> bool:
        """
        Проверяет, есть ли пользователь или одна из его ролей
        в списке исключений.
        """

        # Исключение для конкретного пользователя
        if is_user_allowed(
            member.guild.id,
            member.id
        ):
            return True

        # Исключение для одной из ролей пользователя
        for role in member.roles:
            if is_role_allowed(
                member.guild.id,
                role.id
            ):
                return True

        return False

    # =========================================================
    # Listener: добавление реакции
    # =========================================================

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent
    ):
        # Реакции в личных сообщениях нас не интересуют
        if payload.guild_id is None:
            return

        # Получаем лимит для канала
        limit = get_emoji_limit(
            payload.guild_id,
            payload.channel_id
        )

        # В этом канале лимит не установлен
        if limit is None:
            return

        # Получаем пользователя
        guild = self.bot.get_guild(payload.guild_id)

        if guild is None:
            return

        member = guild.get_member(payload.user_id)

        if member is None:
            try:
                member = await guild.fetch_member(
                    payload.user_id
                )
            except discord.NotFound:
                return
            except discord.HTTPException:
                return

        # Боты не учитываются
        if member.bot:
            return

        # Проверяем исключения
        if self.is_exempt(member):
            return

        try:
            channel = self.bot.get_channel(
                payload.channel_id
            )

            if channel is None:
                return

            # Получаем сообщение
            message = await channel.fetch_message(
                payload.message_id
            )

        except discord.NotFound:
            return

        except discord.Forbidden:
            print(
                f"Нет прав на чтение сообщения "
                f"{payload.message_id}"
            )
            return

        except discord.HTTPException:
            return

        # =====================================================
        # Считаем, сколько реакций этот пользователь
        # уже поставил на данное сообщение
        # =====================================================

        user_reaction_count = 0

        for reaction in message.reactions:
            try:
                async for user in reaction.users():
                    if user.id == member.id:
                        user_reaction_count += 1
                        break

            except discord.HTTPException:
                continue

        # Лимит не превышен
        if user_reaction_count <= limit:
            return

        # =====================================================
        # Лимит превышен.
        # Удаляем именно реакцию, которую пользователь
        # только что добавил.
        # =====================================================

        try:
            await message.remove_reaction(
                payload.emoji,
                member
            )

        except discord.NotFound:
            pass

        except discord.Forbidden:
            print(
                f"Нет прав на удаление реакции "
                f"в канале {payload.channel_id}"
            )

        except discord.HTTPException:
            pass

    # =========================================================
    # Установить лимит
    # =========================================================

    @app_commands.command(
        name="emoji_limit",
        description="Устанавливает лимит реакций в текущем канале"
    )
    @app_commands.describe(
        limit="Максимальное количество реакций от одного пользователя"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def emoji_limit(
        self,
        interaction: discord.Interaction,
        limit: app_commands.Range[int, 0, 50]
    ):
        set_emoji_limit(
            interaction.guild_id,
            interaction.channel.id,
            limit
        )

        await interaction.response.send_message(
            f"Лимит реакций установлен: **{limit}**.",
            ephemeral=True
        )

    # =========================================================
    # Удалить лимит
    # =========================================================

    @app_commands.command(
        name="emoji_limit_remove",
        description="Убирает лимит реакций в текущем канале"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def emoji_limit_remove(
        self,
        interaction: discord.Interaction
    ):
        remove_emoji_limit(
            interaction.guild_id,
            interaction.channel.id
        )

        await interaction.response.send_message(
            "Лимит реакций для этого канала убран.",
            ephemeral=True
        )

    # =========================================================
    # Добавить пользователя в исключения
    # =========================================================

    @app_commands.command(
        name="emoji_allow_user",
        description="Разрешает пользователю ставить неограниченное количество реакций"
    )
    @app_commands.describe(
        user="Пользователь"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def emoji_allow_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):
        add_allowed_user(
            interaction.guild_id,
            user.id
        )

        await interaction.response.send_message(
            f"{user.mention} добавлен в исключения.",
            ephemeral=True
        )

    # =========================================================
    # Убрать пользователя из исключений
    # =========================================================

    @app_commands.command(
        name="emoji_unallow_user",
        description="Убирает пользователя из исключений"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def emoji_unallow_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):
        remove_allowed_user(
            interaction.guild_id,
            user.id
        )

        await interaction.response.send_message(
            f"{user.mention} убран из исключений.",
            ephemeral=True
        )

    # =========================================================
    # Добавить роль в исключения
    # =========================================================

    @app_commands.command(
        name="emoji_allow_role",
        description="Разрешает роли неограниченное количество реакций"
    )
    @app_commands.describe(
        role="Роль"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def emoji_allow_role(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        add_allowed_role(
            interaction.guild_id,
            role.id
        )

        await interaction.response.send_message(
            f"Роль {role.mention} добавлена в исключения.",
            ephemeral=True
        )

    # =========================================================
    # Убрать роль из исключений
    # =========================================================

    @app_commands.command(
        name="emoji_unallow_role",
        description="Убирает роль из исключений"
    )
    @app_commands.checks.has_permissions(
        manage_guild=True
    )
    async def emoji_unallow_role(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        remove_allowed_role(
            interaction.guild_id,
            role.id
        )

        await interaction.response.send_message(
            f"Роль {role.mention} убрана из исключений.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(EmojiLimiter(bot))
