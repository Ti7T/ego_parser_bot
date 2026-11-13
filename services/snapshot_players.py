from database import get_linked_players, save_snapshot
from services import get_player
from dataclasses import asdict
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

async def save_linked_players():
    linked_players = await get_linked_players()
    now = datetime.now(ZoneInfo("Europe/Amsterdam"))
    snapshot_date = (now - timedelta(days=1)).date().isoformat()

    for linked in linked_players:
        try:
            player = await get_player(linked.nick)

            if player is None:
                continue

            player_dict = asdict(player)
            player_json = json.dumps(player_dict, ensure_ascii=False)
            save_snapshot(player.nick, snapshot_date, player_json)

        except Exception as e:
            print(f"Не удалось сохранить данные игрока {linked.nick}: {e}")
    