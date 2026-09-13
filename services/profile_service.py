from api import get_player_json, JSONConverter, url_to_base64_async
from models import Player
from PIL import ImageFont
from config import BASE_URL
from templates import load_template
from typing import Any
import resvg_py
from io import BytesIO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "fonts" / "Inter.ttf"

async def get_player(nick : str) -> Player:
    data = await get_player_json(nick)
    return JSONConverter.to_player(data, BASE_URL)

async def create_profile(player: Player):
    template = load_template("profile.svg")
    data = await make_template_data(player)
    svg = template.render(**data)
    # with open("debug.svg", "w", encoding="utf-8") as f:
    #     f.write(svg)
    png_bytes = resvg_py.svg_to_bytes(
        svg_string=svg,
        font_files=[str(FONT_PATH)]
    )
    return BytesIO(png_bytes)

async def make_template_data(player: Player) -> dict[str, Any]:
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
    # Предположим, что player.best_teammates — это список объектов Teammate
    for tm in player.best_teammates:
        teammates.append({
            "name": tm.nickname,
            "maps": tm.count,
            "avatar_url": await url_to_base64_async(tm.avatar_url)  # если есть, можно использовать в будущем
        })
    
    # 3. Основные данные
    data = {
        "nick": player.nick,
        "rank": player.rank,
        "points": player.points,
        "clan": {
            "name": player.clan.name,
            "avatar_url": await url_to_base64_async(player.clan.avatar_url)
        } if player.clan else None,
        "avatar_url": await url_to_base64_async(player.avatar_url),
        "categories": categories,
        "teammates": teammates,

        "nick_width" : font_nick.getlength(player.nick),
        "points_width" : font_points.getlength(str(player.points))
    }
    
    return data