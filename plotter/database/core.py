import sqlite3
import time
from contextlib import closing
from typing import Optional, Iterable

from plotter.database.dbo import PointDBO, PointListDBO

_connection: Optional[sqlite3.Connection] = None


def _get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        _connection = sqlite3.connect("database.sqlite3")
        _create_schema(_connection)

    return _connection


def _create_schema(conn: sqlite3.Connection) -> None:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chart_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x_value INTEGER NOT NULL,
            y_value INTEGER NOT NULL,
            inserted_at INTEGER NOT NULL
        )
        """)
        conn.commit()


def close_db_connection() -> None:
    if _connection is not None:
        _connection.close()


def delete_all_points() -> int:
    conn = _get_connection()

    with closing(conn.cursor()) as cursor:
        cursor.execute("DELETE FROM chart_data")
        affected_count = cursor.rowcount
        conn.commit()

    return affected_count


def insert_points(points: Iterable[PointDBO]) -> None:
    conn = _get_connection()

    current_timestamp = int(time.time())
    data = tuple((p.x_value, p.y_value, current_timestamp) for p in points)

    with closing(conn.cursor()) as cursor:
        cursor.executemany('INSERT INTO chart_data (x_value, y_value, inserted_at) VALUES (?, ?, ?)', data)
        conn.commit()


def fetch_points_for_chart() -> PointListDBO:
    conn = _get_connection()

    with closing(conn.cursor()) as cursor:
        # Fetch all points
        cursor.execute('SELECT x_value, y_value FROM chart_data ORDER BY inserted_at')
        points = list(PointDBO(x_value=val[0], y_value=val[1]) for val in cursor.fetchall())

        # Fetch last insert timestamp
        cursor.execute("SELECT inserted_at FROM chart_data ORDER BY inserted_at DESC LIMIT 1")
        inserted_at_row = cursor.fetchone()
        inserted_at = inserted_at_row[0] if inserted_at_row is not None else None

    return PointListDBO(inserted_at=inserted_at, points=points)
