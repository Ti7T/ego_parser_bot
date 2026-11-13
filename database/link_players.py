import sqlite3
from .database import get_connection

def init_tables(connection : sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS linked_players (
            user_id INTEGER PRIMARY KEY,
            nick TEXT NOT NULL
        );
    """)


# =========================
# Привязка дискорда к нику
# =========================
def set_linked_player(user_id: int, nick: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO linked_players (user_id, nick)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET nick = excluded.nick
            """,
            (user_id, nick)
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


def get_linked_players() -> str | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT nick
            FROM linked_players
            """
        ).fetchall()

    return row


def remove_linked_player(user_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM linked_players
            WHERE user_id = ?
            """,
            (user_id,)
        )