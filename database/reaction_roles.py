import sqlite3
from .database import get_connection

def init_tables(connection : sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS emoji_roles (
            message_id INTEGER NOT NULL,
            emoji TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (message_id, emoji)
        ) WITHOUT ROWID, STRICT;
    """)


def set_emoji_on_message(message_id : str, emoji : str, role_id : int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO emoji_roles (message_id, emoji, role_id)
            VALUES (?, ?, ?)
            ON CONFLICT(message_id, emoji)
            DO UPDATE SET role_id = excluded.role_id
            """,
            (message_id, emoji, role_id)
        )


def remove_emoji_on_message(message_id : str, emoji : str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM emoji_roles
            WHERE message_id = ? AND emoji = ?
            """,
            (message_id, emoji)
        )


def remove_all_emoji_on_message(message_id : str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM emoji_roles
            WHERE message_id = ?
            """,
            (message_id, )
        )


def get_emoji_role(message_id: str, emoji: str) -> int | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT role_id FROM emoji_roles WHERE message_id = ? AND emoji = ? LIMIT 1",
            (message_id, emoji),
        ).fetchone()
    return row[0] if row is not None else None