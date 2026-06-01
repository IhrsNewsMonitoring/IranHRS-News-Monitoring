"""Database utilities for the news monitoring system.

This module wraps SQLite operations such as creating the messages table,
inserting new entries, and fetching messages for display in the
Streamlit dashboard.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple


def init_db(db_path: str) -> sqlite3.Connection:
    """Initialise the SQLite database and ensure the `messages` table exists.

    The `messages` table stores entries from both Telegram and website
    monitors. Fields include an auto‑incrementing primary key, source
    identifier (e.g. 'telegram' or 'website'), channel or URL, title,
    content, URL, and timestamp.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file. If the file or its parent
        directory does not exist, they will be created.

    Returns
    -------
    sqlite3.Connection
        A connection object with the `messages` table created.
    """
    db_file = Path(db_path)
    # Ensure parent directory exists
    if db_file.parent and not db_file.parent.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Create the messages table if it does not exist
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            channel TEXT,
            title TEXT,
            content TEXT,
            url TEXT,
            date TEXT
        )
        """
    )
    conn.commit()
    return conn


def insert_message(conn: sqlite3.Connection, data: Dict[str, str]) -> None:
    """Insert a single message into the database.

    Parameters
    ----------
    conn : sqlite3.Connection
        Open SQLite database connection.
    data : Dict[str, str]
        Dictionary with keys 'source', 'channel', 'title', 'content', 'url', and 'date'.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO messages (source, channel, title, content, url, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("source"),
            data.get("channel"),
            data.get("title"),
            data.get("content"),
            data.get("url"),
            data.get("date"),
        ),
    )
    conn.commit()


def fetch_messages(conn: sqlite3.Connection, limit: int = 100) -> List[Tuple]:
    """Fetch messages from the database ordered by date descending.

    Parameters
    ----------
    conn : sqlite3.Connection
        Open SQLite database connection.
    limit : int, optional
        Maximum number of rows to return. Defaults to 100.

    Returns
    -------
    List[Tuple]
        A list of database rows, each containing (id, source, channel,
        title, content, url, date).
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT id, source, channel, title, content, url, date FROM messages ORDER BY date DESC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()