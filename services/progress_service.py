from models import Player
from typing import Any
from .render_service import render_svg, svg_to_png
from .player_service import make_player_header_data
from localization import TEXTS
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

async def create_progress_card(
    previous_player: Player,
    current_player: Player,
    days: int,
    language: str = "ru",
):
    data = await make_progress_card_data(
        previous_player,
        current_player,
        days,
        language,
    )

    svg = render_svg("progress_card.svg", data)
    return svg_to_png(svg)


def format_number(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def get_delta(
    before: int,
    now: int,
    *,
    reverse: bool = False,
) -> tuple[str, str]:
    """Возвращает отформатированную разницу и CSS-класс."""
    delta = now - before

    if reverse:
        delta = -delta

    if delta > 0:
        css_class = "pos"
        formatted = f"+{format_number(delta)}"
    elif delta < 0:
        css_class = "neg"
        formatted = f"−{format_number(abs(delta))}"
    else:
        css_class = "neutral"
        formatted = "0"

    return formatted, css_class


def get_total_maps(player: Player) -> int:
    counts = player.counts

    return sum(
        getattr(counts, field)
        for field in (
            "easy", "main", "hard", "insane",
            "extreme", "solo", "jet", "mods",
        )
    )


async def make_progress_card_data(
    previous_player: Player,
    current_player: Player,
    days: int,
    language: str = "ru",
) -> dict[str, Any]:
    labels = TEXTS.get(language, TEXTS["ru"])

    now = datetime.now(ZoneInfo("Europe/Amsterdam")).date()
    start_date = now - timedelta(days=days)

    period_dates = labels["progress_period_dates"].format(
        start_date=start_date.strftime("%d.%m.%Y"),
        end_date=now.strftime("%d.%m.%Y"),
    )

    # Общие показатели
    previous_points = previous_player.points
    current_points = current_player.points

    previous_maps = get_total_maps(previous_player)
    current_maps = get_total_maps(current_player)

    previous_finishes = previous_player.total_finished_maps
    current_finishes = current_player.total_finished_maps

    previous_rank = previous_player.rank
    current_rank = current_player.rank

    # Изменения
    points_delta, points_class = get_delta(
        previous_points, current_points
    )
    maps_delta, maps_class = get_delta(
        previous_maps, current_maps
    )
    finishes_delta, finishes_class = get_delta(
        previous_finishes, current_finishes
    )

    # Для рейтинга уменьшение номера места — улучшение.
    rank_delta, rank_class = get_delta(
        previous_rank, current_rank, reverse=True
    )

    # Главный результат — изменение очков.
    main_delta, main_class = get_delta(
        previous_points, current_points
    )

    data = await make_player_header_data(current_player)

    data.update({
        "avatar_initial": current_player.nick[:1].upper(),

        # Главный результат
        "current_points": format_number(
            current_points - previous_points
        ),
        "previous_points": format_number(previous_points),
        "main_delta": main_delta,
        "main_delta_class": main_class,
        "progress_width": 566,

        # Показатели за период
        "points_now": format_number(current_points),
        "points_before": format_number(previous_points),
        "points_delta": points_delta,
        "points_delta_class": points_class,

        "maps_now": format_number(current_maps),
        "maps_before": format_number(previous_maps),
        "maps_delta": maps_delta,
        "maps_delta_class": maps_class,

        "clears_now": format_number(current_finishes),
        "clears_before": format_number(previous_finishes),
        "clears_delta": finishes_delta,
        "clears_delta_class": finishes_class,

        "rank_now": current_rank,
        "rank_before": previous_rank,
        "rank_delta": rank_delta,
        "rank_delta_class": rank_class,

        # Общие показатели
        "lifetime_points_before": format_number(previous_points),
        "lifetime_points_now": format_number(current_points),
        "lifetime_points_delta": points_delta,

        "lifetime_maps_before": format_number(previous_maps),
        "lifetime_maps_now": format_number(current_maps),
        "lifetime_maps_delta": maps_delta,

        # Локализация
        "text_overall_score": labels["progress_overall_score"],
        "text_player_progress": labels["progress_player"],
        "period_title": labels["progress_period_title"],
        "period_dates": period_dates,

        "text_main_result": labels["progress_main_result"],
        "text_points_earned": labels["progress_points_earned"],
        "text_current_period": labels["progress_current_period"],
        "text_previous_period": labels["progress_previous_period"],
        "text_vs_previous": labels["progress_vs_previous"],

        "text_period_metrics": labels["progress_period_metrics"],
        "text_points": labels["progress_points"],
        "text_maps": labels["progress_maps"],
        "text_finishes": labels["progress_finishes"],
        "text_rank": labels["progress_rank"],

        "text_before_prefix": labels["progress_before"],
        "text_was": labels["progress_was"],
        "text_now": labels["progress_now"],

        "text_overall_metrics": labels["progress_overall_metrics"],
        "text_points_all_time": labels["progress_points_all_time"],
        "text_maps_all_time": labels["progress_maps_all_time"],

        "text_period_comparison": labels["progress_comparison"],
        "text_brand": "EGO PLAYER STATISTICS",
        "footer_note": labels["progress_footer"],

        # Подсказки
        "points_hint": labels["progress_points_hint"],
        "maps_hint": labels["progress_maps_hint"],
        "clears_hint": labels["progress_finishes_hint"],
        "rank_hint": labels["progress_rank_hint"],
    })

    return data
    

