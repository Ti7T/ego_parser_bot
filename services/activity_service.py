from collections import Counter
from datetime import datetime, timedelta, timezone
from io import BytesIO
from typing import Any

from models import Player
from math import ceil
from .player_service import make_player_header_data
from .render_service import render_svg, svg_to_png


ACTIVITY_SQUARE_SIZE = 35
ACTIVITY_STEP = 40

ACTIVITY_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

ACTIVITY_LEGEND = [
    {"level": 0, "label": "0"},
    {"level": 1, "label": "1–2"},
    {"level": 2, "label": "3–5"},
    {"level": 3, "label": "6+"},
]

TIME_TICK_MIN_DISTANCE = 100 / 850


async def create_activity_graphs(player: Player) -> BytesIO:
    data = await make_activity_graphs_data(player)
    svg = render_svg("activity_graphs.svg", data)
    return svg_to_png(svg)


def create_points_history(
    player: Player,
) -> tuple[list[dict[str, Any]], list[int], int]:
    history = sorted(
        (item for item in player.point_history if item.points > 0),
        key=lambda item: item.finished_at,
    )

    point_history: list[dict[str, Any]] = []
    current_points = 0

    if history:
        first_date = datetime.fromisoformat(history[0].finished_at)
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

    return point_history, create_point_ticks(point_max), point_max


def create_point_ticks(point_max: int) -> list[int]:
    if point_max <= 0:
        return [0]

    step = ceil(point_max / 4)
    ticks = list(range(0, point_max, step))

    ticks.append(point_max)
    return ticks


def create_time_ticks(
    point_history: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not point_history:
        return []

    first_date = datetime.fromisoformat(point_history[0]["finished_at"])
    last_date = datetime.fromisoformat(point_history[-1]["finished_at"])
    total_seconds = (last_date - first_date).total_seconds()

    time_ticks = [{
        "position": 0,
        "label": first_date.strftime("%d.%m"),
    }]

    current = first_date.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    if current <= first_date:
        current = next_month(current)

    while current < last_date:
        position = (
            (current - first_date).total_seconds() / total_seconds
            if total_seconds > 0
            else 0
        )

        time_ticks.append({
            "position": position,
            "label": current.strftime("%m.%Y"),
        })

        current = next_month(current)

    time_ticks.append({
        "position": 1,
        "label": last_date.strftime("%d.%m"),
    })

    return filter_time_ticks(time_ticks)


def next_month(date: datetime) -> datetime:
    return (date.replace(day=28) + timedelta(days=4)).replace(day=1)


def filter_time_ticks(
    time_ticks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if len(time_ticks) <= 2:
        return time_ticks

    filtered_ticks = [time_ticks[0]]

    for tick in time_ticks[1:-1]:
        if (
            tick["position"] - filtered_ticks[-1]["position"]
            >= TIME_TICK_MIN_DISTANCE
        ):
            filtered_ticks.append(tick)

    filtered_ticks.append(time_ticks[-1])
    return filtered_ticks


def create_activity_counter(player: Player) -> Counter[str]:
    unique_records = {}

    for record in player.point_history:
        key = (record.map_id, record.finished_at)
        unique_records[key] = record

    activity_counter: Counter[str] = Counter()

    for record in unique_records.values():
        activity_counter[record.finished_at[:10]] += 1

    return activity_counter


def create_activity_weeks(
    activity_counter: Counter[str],
) -> list[dict[str, Any]]:
    latest_date = datetime.now().date()

    # Week ends on Sunday.
    days_until_sunday = 6 - latest_date.weekday()
    end_date = latest_date + timedelta(days=days_until_sunday)
    start_date = end_date - timedelta(weeks=20, days=6)

    activity_weeks = []
    current_week = start_date

    while current_week <= end_date:
        days = []

        for i in range(7):
            current_day = current_week + timedelta(days=i)
            date_key = current_day.isoformat()

            days.append({
                "date": date_key,
                "count": activity_counter.get(date_key, 0),
            })

        activity_weeks.append({
            "label": current_week.strftime("%d.%m"),
            "days": days,
        })

        current_week += timedelta(days=7)

    return activity_weeks


async def make_activity_graphs_data(
    player: Player,
) -> dict[str, Any]:
    point_history, point_ticks, point_max = create_points_history(player)
    time_ticks = create_time_ticks(point_history)

    activity_counter = create_activity_counter(player)
    activity_weeks = create_activity_weeks(activity_counter)

    data = await make_player_header_data(player)

    data.update({
        "point_history": point_history,
        "point_ticks": point_ticks,
        "point_max": point_max,
        "time_ticks": time_ticks,
        "activity_weeks": activity_weeks,
        "activity_days": ACTIVITY_DAYS,
        "activity_square": ACTIVITY_SQUARE_SIZE,
        "activity_step": ACTIVITY_STEP,
        "activity_legend": ACTIVITY_LEGEND,
    })

    return data
