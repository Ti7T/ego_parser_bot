from api import url_to_base64_async
from models import Player
from PIL import ImageFont
from typing import Any
from .render_service import FONT_PATH, render_svg, svg_to_png
from .player_service import make_player_header_data

async def create_profile(player: Player):
    data = await make_profile_data(player)
    svg = render_svg("profile.svg", data)
    # with open("debug.svg", "w", encoding="utf-8") as f:
    #     f.write(svg)
    return svg_to_png(svg)


async def make_profile_data(player: Player) -> dict[str, Any]:
    # 1. Категории: список словарей для каждого уровня сложности
    categories = []
    # Список полей в том же порядке, что и в SVG (Easy, Main, Hard, Insane, Extreme, Jet, Solo, Mods)
    difficulty_fields = ["easy", "main", "hard", "insane", "extreme", "jet", "solo", "mods"]
    font_nick = ImageFont.truetype(FONT_PATH, 42)   # размер как в SVG
    font_points = ImageFont.truetype(FONT_PATH, 30)

    # Для красоты можно сохранить названия с большой буквы (как в интерфейсе)
    display_names = {
        "easy": "Easy",
        "main": "Main",
        "hard": "Hard",
        "insane": "Insane",
        "extreme": "Extreme",
        "jet": "Jet",
        "solo": "Solo",
        "mods": "Mods"
    }
    
    for field in difficulty_fields:
        completed = getattr(player.counts, field)
        total = getattr(player.counts_total, field)
        percent = round((completed / total * 100) if total > 0 else 0, 1)
        categories.append({
            "name": display_names[field],
            "percent": percent,
            "completed": completed,
            "total": total
        })
    
    # 2. Тиммейты: список словарей
    teammates = []
    for tm in player.best_teammates:
        teammates.append({
            "name": tm.nickname,
            "maps": tm.count,
            "avatar_url": await url_to_base64_async(tm.avatar_url) 
        })
    
    # 3. Основные данные
    data = await make_player_header_data(player=player)

    data.update({
        "categories": categories,
        "teammates": teammates,
        "nick_width": font_nick.getlength(player.nick),
        "points_width": font_points.getlength(str(player.points)),
        "playtime": round(player.total_playtime / 3600, 1)
    })

    return data

