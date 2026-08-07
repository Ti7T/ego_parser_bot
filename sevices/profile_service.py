from api import get_player_json, JSONConverter, http_session
from models import Player
from config import EGO_API_URL, APIEndpoints

async def get_player(nick : str) -> Player:
  data = await get_player_json(nick, http_session)
  return JSONConverter.to_player(data, EGO_API_URL)