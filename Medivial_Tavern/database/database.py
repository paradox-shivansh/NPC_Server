import sqlite3

from pathlib import Path


def get_connection(npc_id: str):

    database_folder = Path("data") / npc_id

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