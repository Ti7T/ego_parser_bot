import discord
from discord.ext import commands
from discord import app_commands
from database import get_emoji_role, set_emoji_on_message, remove_emoji_on_message, remove_all_emoji_on_message
from utils import serialize_emoji
import json
from localization import t

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # =========================================================
    # Listener: добавление реакции
    # =========================================================

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent
    ):
        if payload.member.bot:
            return
        message_id = payload.message_id
        emoji = serialize_emoji(payload.emoji)

        emoji_role_id = get_emoji_role(message_id, emoji)

        if not emoji_role_id:
            return

        member = payload.member
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(emoji_role_id)
        await member.add_roles(role)

        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self,
        payload: discord.RawReactionActionEvent
    ):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None:
            return
        if member.bot:
            return 
        message_id = payload.message_id
        emoji = serialize_emoji(payload.emoji)

        emoji_role_id = get_emoji_role(message_id, emoji)

        if not emoji_role_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(emoji_role_id)
        await member.remove_roles(role)
    

    
    @app_commands.command(
        name="reaction_roles_create",
        description="Создать сообщение для выдачи ролей / Create a reaction-role message"
    )
    @app_commands.describe(
        config="Конфигурация сообщения в JSON / Message configuration in JSON"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reaction_roles_create(
        self,
        interaction: discord.Interaction,
        config: str
    ):
        try:
            data = json.loads(config)

            title = data["title"]
            description = data["description"]
            roles = data["roles"]

            if not isinstance(title, str) or not isinstance(description, str):
                raise ValueError(t(interaction.user.id, "json_title_type"))

            if not isinstance(roles, list):
                raise ValueError(t(interaction.user.id, "json_roles_type"))

            for role_data in roles:
                if not isinstance(role_data, dict):
                    raise ValueError(t(interaction.user.id, "json_role_object"))

                if not isinstance(role_data.get("role_id"), int):
                    raise ValueError(t(interaction.user.id, "json_role_id"))

                if not isinstance(role_data.get("emoji"), str):
                    raise ValueError(t(interaction.user.id, "json_emoji"))

                if not isinstance(role_data.get("description"), str):
                    raise ValueError(t(interaction.user.id, "json_role_description"))

        except (json.JSONDecodeError, KeyError, ValueError) as error:
            await interaction.response.send_message(
                t(interaction.user.id, "reaction_json_error", error=error),
                ephemeral=True
            )
            return

        container = discord.ui.Container()

        container.add_item(
            discord.ui.TextDisplay(f"# {title}")
        )

        container.add_item(
            discord.ui.TextDisplay(f"## {description}")
        )

        container.add_item(
            discord.ui.Separator(
                spacing=discord.SeparatorSpacing.large
            )
        )

        valid_roles = []

        for role_data in roles:
            role = interaction.guild.get_role(role_data["role_id"])

            if role is None:
                continue

            valid_roles.append((role, role_data))

        for index, (role, role_data) in enumerate(valid_roles):
            container.add_item(
                discord.ui.TextDisplay(
                    f"### {role_data['emoji']} {role.mention}\n"
                    f"{role_data['description']}"
                )
            )

            if index < len(valid_roles) - 1:
                container.add_item(
                    discord.ui.Separator(
                        spacing=discord.SeparatorSpacing.small
                    )
                )

        container.add_item(
            discord.ui.Separator(
                spacing=discord.SeparatorSpacing.large
            )
        )

        container.add_item(
            discord.ui.TextDisplay(
                t(interaction.user.id, "reaction_footer")
            )
        )

        view = discord.ui.LayoutView()
        view.add_item(container)

        await interaction.response.defer(ephemeral=True)

        await interaction.channel.send(view=view)

        await interaction.followup.send(
            t(interaction.user.id, "reaction_published"),
            ephemeral=True
        )


    @app_commands.command(
        name="reaction_roles_add",
        description="Привязать реакцию к роли / Link a reaction to a role"
    )
    @app_commands.describe(
        message_id="ID сообщения / Message ID",
        emoji="Эмодзи реакции / Reaction emoji",
        role="Выдаваемая роль / Role to assign"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reaction_roles_add(
        self,
        interaction: discord.Interaction,
        message_id: str,
        emoji: str,
        role: discord.Role
    ):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            set_emoji_on_message(message_id, emoji, role.id)
        except discord.NotFound:
            await interaction.response.send_message(
                t(interaction.user.id, "message_not_found"), ephemeral=True
            )
            return
        except discord.Forbidden:
            await interaction.response.send_message(
                t(interaction.user.id, "bot_no_access"), ephemeral=True
            )
            return
        
        await message.add_reaction(emoji)
        await interaction.response.send_message(
            t(interaction.user.id, "reaction_added", emoji=emoji),
            ephemeral=True
        )

    @app_commands.command(
        name="reaction_roles_remove",
        description="Убрать привязку реакции к роли / Remove a reaction-role link"
    )
    @app_commands.describe(
        message_id="ID сообщения / Message ID",
        emoji="Эмодзи реакции / Reaction emoji"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reaction_roles_remove(
        self,
        interaction: discord.Interaction,
        message_id: str,
        emoji: str,
    ):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            remove_emoji_on_message(message_id, emoji)
        except discord.NotFound:
            await interaction.response.send_message(
                t(interaction.user.id, "message_not_found"), ephemeral=True
            )
            return
        except discord.Forbidden:
            await interaction.response.send_message(
                t(interaction.user.id, "bot_no_access"), ephemeral=True
            )
            return
        
        await message.remove_reaction(emoji)
        await interaction.response.send_message(
            t(interaction.user.id, "reaction_removed", emoji=emoji),
            ephemeral=True
        )

    @app_commands.command(
        name="reaction_roles_remove_all",
        description="Убрать все привязки реакций сообщения / Remove all reaction-role links"
    )
    @app_commands.describe(
        message_id="ID сообщения / Message ID"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reaction_roles_remove_all(
        self,
        interaction: discord.Interaction,
        message_id: str
    ):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            remove_all_emoji_on_message(message_id)
        except discord.NotFound:
            await interaction.response.send_message(
                t(interaction.user.id, "message_not_found"), ephemeral=True
            )
            return
        except discord.Forbidden:
            await interaction.response.send_message(
                t(interaction.user.id, "bot_no_access"), ephemeral=True
            )
            return
        
        await message.clear_reactions()
        await interaction.response.send_message(
            t(interaction.user.id, "reactions_removed"),
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
