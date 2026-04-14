from pathlib import Path
import sqlite3


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "cricbuzz_livestats.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize_database(force: bool = False) -> None:
    from utils.db_setup import initialize_database as _initialize_database

    _initialize_database(force=force)


def store_api_match_snapshots(matches: list[dict], source: str = "notebook") -> int:
    from utils.db_setup import store_api_match_snapshots as _store_api_match_snapshots

    with get_connection() as connection:
        inserted = _store_api_match_snapshots(connection, matches, source=source)
        connection.commit()
        return inserted
