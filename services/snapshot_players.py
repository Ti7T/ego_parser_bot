from dataclasses import asdict
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from database import get_linked_players, save_snapshot
from .player_service import get_player
from .exceptions import PlayerNotFoundError


async def save_linked_players():
    linked_players = get_linked_players()

    now = datetime.now(ZoneInfo("Europe/Moscow"))
    snapshot_date = (now - timedelta(days=1)).date().isoformat()

    for nick in linked_players:
        try:
            player = await get_player(nick)

            player_json = json.dumps(
                asdict(player),
                ensure_ascii=False
            )

            save_snapshot(player.nick, snapshot_date, player_json)

        except PlayerNotFoundError:
            print(f"Игрок {nick} не найден")

        except Exception as e:
            print(f"Не удалось сохранить данные игрока {nick}: {e}")
