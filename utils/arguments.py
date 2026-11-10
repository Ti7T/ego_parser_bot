from discord import Interaction, Member
from database import get_linked_player

async def resolve_nick_argument(
    nick: str | None,
    member: Member | None,
    interaction: Interaction
) -> str | None:

    if nick is not None and member is not None:
        await interaction.response.send_message(
            "Укажи либо игровой ник, либо Discord-пользователя, но не оба варианта.",
            ephemeral=True
        )
        return None

    if nick is not None:
        return nick

    user_id = member.id if member is not None else interaction.user.id
    linked_nick = get_linked_player(user_id)

    if linked_nick is None:
        await interaction.response.send_message(
            "❌ У пользователя не привязан игровой ник.\n"
            "Используйте `/link`, чтобы привязать его.",
            ephemeral=True
        )
        return None

    return linked_nick