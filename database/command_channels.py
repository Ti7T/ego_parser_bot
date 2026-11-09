import sqlite3
from .database import get_connection

def init_tables(connection : sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS command_channels (
            guild_id INTEGER PRIMARY KEY,
            channel_id INTEGER NOT NULL
        );
    """)


# =========================
# Канал для команд
# =========================

def set_command_channel(guild_id: int, channel_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO command_channels (guild_id, channel_id)
            VALUES (?, ?)
            ON CONFLICT(guild_id)
            DO UPDATE SET channel_id = excluded.channel_id
            """,
            (guild_id, channel_id)
        )


def get_command_channel(guild_id: int) -> int | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT channel_id
            FROM command_channels
            WHERE guild_id = ?
            """,
            (guild_id,)
        ).fetchone()

    if row is None:
        return None

    return row["channel_id"]


def remove_command_channel(guild_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM command_channels
            WHERE guild_id = ?
            """,
            (guild_id,)
        )