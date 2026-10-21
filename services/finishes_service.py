from models import Player
from .player_service import make_player_header_data
from .render_service import render_svg, svg_to_png
from io import BytesIO
from typing import Any

async def create_recent_finishes(
    player: Player,
) -> BytesIO:
    data = await make_recent_finishes_data(player)
    svg = render_svg("recent_finishes.svg", data)
    return svg_to_png(svg)

async def make_recent_finishes_data(
    player: Player,
) -> dict[str, Any]:

    finishes = []

    for record in player.activity_records[:10]:
        finishes.append({
            "map_name": record.map_name,
            "time": record.time,
            "rank": record.rank,
            "points": record.points,
            "difficulty": record.difficulty,
            "stars": record.stars,
            "is_team": record.is_team,
            "is_solo_team": record.is_solo_team,
            "is_refinish": record.is_refinish,
            "finished_at": record.finished_at,
        })

    data = await make_player_header_data(player)

    data.update({
        "playtime": round(player.total_playtime / 3600, 1),
        "finishes": finishes
    })

    return data
