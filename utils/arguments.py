from discord import Interaction
from database import get_linked_player

async def resolve_nick_argument(
    nick: str | None, 
    interaction: Interaction
) -> str | None:

    if nick is not None:
        return nick
    
    nick = get_linked_player(interaction.user.id)
    if nick is None:
        await interaction.response.send_message(
            "❌ У тебя не привязан игровой ник.\n"
            "Используй `/link`, чтобы привязать его.",
            ephemeral=True
        )
        return None
        
    return nick