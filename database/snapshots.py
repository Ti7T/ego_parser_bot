import sqlite3
from .database import get_connection


def init_tables(connection : sqlite3.Connection) -> None:
    connection.executescript("""
        CREATE TABLE player_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nick TEXT NOT NULL,
            snapshot_date TEXT NOT NULL,
            data TEXT NOT NULL,

            UNIQUE(nick, snapshot_date)
        );
    """)


def save_snapshot(nick : str, snapshot_date : str, data : str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO player_snapshots (nick, snapshot_date, data)
            VALUES (?, ?, ?)
            """,
            (nick, snapshot_date, data)
        )