from models import Player
from .svg_loader import load_svg_text
from .image_loader import url_to_base64
from typing import Any
import cairosvg
from io import BytesIO
from PIL import ImageFont


def make_template_data(player: Player) -> dict[str, Any]:
    # 1. Категории: список словарей для каждого уровня сложности
    categories = []
    # Список полей в том же порядке, что и в SVG (Easy, Main, Hard, Insane, Extreme, Jet, Solo, Mods)
    difficulty_fields = ["easy", "main", "hard", "insane", "extreme", "jet", "solo", "mods"]
    font_nick = ImageFont.truetype("segoeui.ttf", 42)   # размер как в SVG
    font_points = ImageFont.truetype("segoeui.ttf", 30)

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
            "avatar_url": url_to_base64(tm.avatar_url)  # если есть, можно использовать в будущем
        })
    
    # 3. Основные данные
    data = {
        "nick": player.nick,
        "rank": player.rank,
        "points": player.points,
        "avatar_url": url_to_base64(player.avatar_url),
        "categories": categories,
        "teammates": teammates,

        "nick_width" : font_nick.getlength(player.nick),
        "points_width" : font_points.getlength(str(player.points))
    }
    
    return data

def profile_image_create(player: Player):
  template = load_svg_text("templates/profile.svg")
  data = make_template_data(player)
  svg = template.render(**data)
  png_bytes = cairosvg.svg2png(
    bytestring=svg.encode('utf-8'),
  )
  return BytesIO(png_bytes)
