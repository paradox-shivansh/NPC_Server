import sqlite3

from pathlib import Path


BASE_DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def get_connection(npc_id: str):

    database_folder = BASE_DATA_DIR / npc_id

    database_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    database_path = database_folder / "memory.db"

    connection = sqlite3.connect(
        database_path
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database(npc_id: str):

    conn = get_connection(npc_id)

    cursor = conn.cursor()

    # ENTITY MEMORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity TEXT NOT NULL,
            fact TEXT NOT NULL,
            importance REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # REFLECTION MEMORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflection_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson TEXT NOT NULL,
            importance REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # SUMMARY MEMORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summary_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # CHARACTER MEMORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS character_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            traits TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()