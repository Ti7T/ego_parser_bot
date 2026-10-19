import json
from api import get_player_json, JSONConverter, get_player_playtime_json
from api import url_to_base64_async
from models import Player
from typing import Any
from config import BASE_URL
from .exceptions import PlayerNotFoundError


async def get_player(nick: str) -> Player:
    data = await get_player_json(nick)
    if not data or data.get("error") == "player not found":
        raise PlayerNotFoundError(nick)
    playtime = await get_player_playtime_json(nick)
    if not playtime or playtime.get("error") == "player not found":
        raise PlayerNotFoundError(nick)
    data["playtime"] = playtime
    return JSONConverter.to_player(data, BASE_URL)

async def make_player_header_data(player: Player) -> dict[str, Any]:
    return {
        "nick": player.nick,
        "rank": player.rank,
        "points": player.points,
        "clan": {
            "name": player.clan.name,
            "avatar_url": await url_to_base64_async(player.clan.avatar_url)
        } if player.clan else None,
        "avatar_url": await url_to_base64_async(player.avatar_url)
    }