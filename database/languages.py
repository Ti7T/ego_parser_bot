from .database import get_connection


def init_tables(connection) -> None:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS user_languages (
            user_id INTEGER PRIMARY KEY,
            language TEXT NOT NULL DEFAULT 'ru'
                CHECK(language IN ('ru', 'en'))
        )
    """)


def get_user_language(user_id: int) -> str:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT language FROM user_languages WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    return row["language"] if row else "ru"


def set_user_language(user_id: int, language: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO user_languages (user_id, language)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET language = excluded.language
            """,
            (user_id, language),
        )
