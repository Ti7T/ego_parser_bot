import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "bot.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database() -> None:
    with get_connection() as connection:
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

            CREATE TABLE IF NOT EXISTS command_channels (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER NOT NULL
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