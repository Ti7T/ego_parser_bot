from api import get_player_json, JSONConverter, url_to_base64_async, get_player_playtime_json
from models import Player
from PIL import ImageFont
from config import BASE_URL
from templates import load_template
from typing import Any
import resvg_py
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import Counter
import json

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "fonts" / "Inter.ttf"

async def get_player(nick : str) -> Player:
    data = await get_player_json(nick)
    data["playtime"] = await get_player_playtime_json(nick)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return JSONConverter.to_player(data, BASE_URL)

def svg_to_png(svg: str) -> BytesIO:
    png_bytes = resvg_py.svg_to_bytes(
        svg_string=svg,
        font_files=[str(FONT_PATH)],
    )
    return BytesIO(png_bytes)

def render_svg(template_name: str, data: dict[str, Any]) -> str:
    template = load_template(template_name)
    return template.render(**data)

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
        "points_width" : font_points.getlength(str(player.points)),
        "playtime" : round(player.total_playtime / 3600, 1)
    }

    return data

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

    return {
        "nick": player.nick,
        "rank": player.rank,
        "points": player.points,
        "avatar_url": await url_to_base64_async(player.avatar_url),

        "clan": (
            {
                "name": player.clan.name,
                "avatar_url": await url_to_base64_async(
                    player.clan.avatar_url
                ),
            }
            if player.clan
            else None
        ),
        "playtime" : round(player.total_playtime / 3600, 1),
        "finishes": finishes,
    }

async def make_activity_graphs_data(
    player: Player,
) -> dict[str, Any]:

    # -------------------------
    # POINTS HISTORY
    # -------------------------

    point_history = []
    current_points = 0

    history = sorted(
        (
            item
            for item in player.point_history
            if item.points > 0
        ),
        key=lambda item: item.finished_at,
    )

    if history:
        first_date = datetime.fromisoformat(
            history[0].finished_at
        )

        first_finished_at = (
            first_date - timedelta(days=1)
        ).strftime("%Y-%m-%d %H:%M:%S")

        point_history.append({
            "finished_at": first_finished_at,
            "timestamp": datetime.fromisoformat(
                first_finished_at
            ).replace(tzinfo=timezone.utc).timestamp(),
            "points": 0,
        })
    
    for item in history:
        current_points += item.points

        point_history.append({
            "finished_at": item.finished_at,
            "timestamp": datetime.fromisoformat(
                item.finished_at
            ).replace(tzinfo=timezone.utc).timestamp(),
            "points": current_points,
        })

    point_max = max(
        (item["points"] for item in point_history),
        default=0,
    )

    if point_max == 0:
        point_ticks = [0]
    else:
        step = max(1, round(point_max / 4))

        point_ticks = [
            0,
            step,
            step * 2,
            step * 3,
            point_max,
        ]

    # -------------------------
    # X-AXIS
    # -------------------------

    time_ticks = []

    if point_history:
        first_date = datetime.fromisoformat(
            point_history[0]["finished_at"]
        )
        last_date = datetime.fromisoformat(
            point_history[-1]["finished_at"]
        )

        total_seconds = (
            last_date - first_date
        ).total_seconds()

        # Начало периода
        time_ticks.append({
            "position": 0,
            "label": first_date.strftime("%d.%m"),
        })

        # Начало каждого месяца
        current = (
            first_date.replace(
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        )

        if current <= first_date:
            current = (
                current.replace(day=28)
                + timedelta(days=4)
            ).replace(day=1)

        while current < last_date:

            position = (
                (current - first_date).total_seconds()
                / total_seconds
                if total_seconds > 0
                else 0
            )

            time_ticks.append({
                "position": position,
                "label": current.strftime("%m.%Y"),
            })

            current = (
                current.replace(day=28)
                + timedelta(days=4)
            ).replace(day=1)

        # Конец периода
        time_ticks.append({
            "position": 1,
            "label": last_date.strftime("%d.%m"),
        })

        # Не даём подписям налезать друг на друга.
        min_distance = 100 / 850

        filtered_ticks = [time_ticks[0]]

        for tick in time_ticks[1:-1]:
            if (
                tick["position"]
                - filtered_ticks[-1]["position"]
                >= min_distance
            ):
                filtered_ticks.append(tick)

        # Последнюю дату всегда оставляем
        filtered_ticks.append(time_ticks[-1])

        time_ticks = filtered_ticks

    # -------------------------
    # MAP ACTIVITY
    # -------------------------

    # Убираем точные дубли одного события.
    unique_records = {}

    for record in player.point_history:
        key = (
            record.map_id,
            record.finished_at,
        )

        unique_records[key] = record

    activity_counter = Counter()

    for record in unique_records.values():
        date = record.finished_at[:10]
        activity_counter[date] += 1

    # -------------------------
    # LAST 21 WEEKS
    # -------------------------

    latest_date = datetime.now().date()

    # Неделя заканчивается воскресеньем.
    days_until_sunday = 6 - latest_date.weekday()

    end_date = latest_date + timedelta(
        days=days_until_sunday
    )

    start_date = end_date - timedelta(
        weeks=20,
        days=6,
    )

    activity_weeks = []

    current_week = start_date

    while current_week <= end_date:

        days = []

        for i in range(7):
            current_day = (
                current_week + timedelta(days=i)
            )

            date_key = current_day.isoformat()

            days.append({
                "date": date_key,
                "count": activity_counter.get(
                    date_key,
                    0,
                ),
            })

        activity_weeks.append({
            "label": current_week.strftime("%d.%m"),
            "days": days,
        })

        current_week += timedelta(days=7)

    # -------------------------
    # FINAL DATA
    # -------------------------

    return {
        "nick": player.nick,
        "rank": player.rank,
        "points": player.points,

        "avatar_url": await url_to_base64_async(
            player.avatar_url
        ),

        "clan": (
            {
                "name": player.clan.name,
                "avatar_url": await url_to_base64_async(
                    player.clan.avatar_url
                ),
            }
            if player.clan
            else None
        ),

        "point_history": point_history,
        "point_ticks": point_ticks,
        "point_max": point_max,
        "time_ticks": time_ticks,

        "activity_weeks": activity_weeks,
        "activity_days": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ],

        "activity_square": 35,
        "activity_step": 40,

        "activity_legend": [
            {"level": 0, "label": "0"},
            {"level": 1, "label": "1–2"},
            {"level": 2, "label": "3–5"},
            {"level": 3, "label": "6+"},
        ],
    }


async def create_activity_graphs(
    player: Player,
) -> BytesIO:

    data = await make_activity_graphs_data(player)
    svg = render_svg("activity_graphs.svg", data)

    return svg_to_png(svg)