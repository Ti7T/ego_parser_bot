import sqlite3
from .database import get_connection

def init_tables(connection : sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS fire_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nick TEXT NOT NULL,
            game_date TEXT NOT NULL,
            current INTEGER NOT NULL,
            done_today BOOLEAN NOT NULL,
            best INTEGER NOT NULL,
            badge BOOLEAN NOT NULL DEFAULT FALSE,

            UNIQUE(nick, game_date)
        );
    """)


def set_fire_history(
        nick: str, 
        game_date : str,
        current: int,
        best: int,
        done_today: bool,
        badge: bool
    ) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO fire_history (nick, game_date, current, best, done_today, badge)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(nick, game_date)
            DO UPDATE SET
                current = excluded.current,
                best = excluded.best,
                done_today = MAX(fire_history.done_today, excluded.done_today),
                badge = excluded.badge
            """,
            (nick, game_date, current, best, done_today, badge)
        )


def get_linked_player(user_id: int) -> str | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT nick
            FROM linked_players
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

    if row is None:
        return None

    return row["nick"]


def get_fire_history(nick: str, game_date: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT current, best, done_today, badge
            FROM fire_history
            WHERE nick = ? AND game_date = ?
            LIMIT 1
            """,
            (nick, game_date)
        ).fetchone()

    if row is None:
        return None

    return {
        "current": row["current"],
        "best": row["best"],
        "done_today": bool(row["done_today"]),
        "badge": bool(row["badge"])
    }


def get_fire_dates(nick: str, start_date: str, end_date: str) -> set[str]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT game_date
            FROM fire_history
            WHERE nick = ?
              AND game_date BETWEEN ? AND ?
              AND done_today = 1
            """,
            (nick, start_date, end_date)
        ).fetchall()

    return {row["game_date"] for row in rows}