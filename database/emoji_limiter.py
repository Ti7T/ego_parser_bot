import sqlite3
from .database import get_connection

def init_tables(connection : sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS emoji_limits (
            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            emoji_limit INTEGER NOT NULL,
            PRIMARY KEY (guild_id, channel_id)
        );

        CREATE TABLE IF NOT EXISTS emoji_allowed_users (
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS emoji_allowed_roles (
            guild_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, role_id)
        );
    """)

# =========================
# Ограничение эмодзи
# =========================

def set_emoji_limit(guild_id: int, channel_id: int, emoji_limit: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO emoji_limits (guild_id, channel_id, emoji_limit)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id, channel_id)
            DO UPDATE SET emoji_limit = excluded.emoji_limit
            """,
            (guild_id, channel_id, emoji_limit)
        )


def get_emoji_limit(guild_id: int, channel_id: int) -> int | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT emoji_limit
            FROM emoji_limits
            WHERE guild_id = ? AND channel_id = ?
            """,
            (guild_id, channel_id)
        ).fetchone()

    if row is None:
        return None

    return row["emoji_limit"]


def remove_emoji_limit(guild_id: int, channel_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM emoji_limits
            WHERE guild_id = ? AND channel_id = ?
            """,
            (guild_id, channel_id)
        )


# =========================
# Пользователи-исключения
# =========================

def add_allowed_user(guild_id: int, user_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO emoji_allowed_users
            (guild_id, user_id)
            VALUES (?, ?)
            """,
            (guild_id, user_id)
        )


def remove_allowed_user(guild_id: int, user_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM emoji_allowed_users
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        )


def is_user_allowed(guild_id: int, user_id: int) -> bool:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT 1
            FROM emoji_allowed_users
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

    return row is not None


# =========================
# Роли-исключения
# =========================

def add_allowed_role(guild_id: int, role_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO emoji_allowed_roles
            (guild_id, role_id)
            VALUES (?, ?)
            """,
            (guild_id, role_id)
        )


def remove_allowed_role(guild_id: int, role_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM emoji_allowed_roles
            WHERE guild_id = ? AND role_id = ?
            """,
            (guild_id, role_id)
        )


def is_role_allowed(guild_id: int, role_id: int) -> bool:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT 1
            FROM emoji_allowed_roles
            WHERE guild_id = ? AND role_id = ?
            """,
            (guild_id, role_id)
        ).fetchone()

    return row is not None
