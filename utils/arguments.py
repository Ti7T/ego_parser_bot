from discord import Interaction, Member

from database import get_linked_player
from localization import t


async def resolve_nick_argument(
    nick: str | None,
    member: Member | None,
    interaction: Interaction,
) -> str | None:
    user_id = interaction.user.id

    if nick is not None and member is not None:
        await interaction.response.send_message(
            t(user_id, "nick_both"),
            ephemeral=True,
        )
        return None

    if nick is not None:
        return nick

    target_user_id = member.id if member is not None else user_id
    linked_nick = get_linked_player(target_user_id)

    if linked_nick is None:
        await interaction.response.send_message(
            t(user_id, "not_linked"),
            ephemeral=True,
        )
        return None

    return linked_nick
