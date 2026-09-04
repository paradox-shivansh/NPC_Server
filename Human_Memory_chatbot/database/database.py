import sqlite3
from pathlib import Path


DB_PATH = Path("database/chatbot_memory.db")


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # -------------------------
    # ENTITY MEMORY
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entity_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT NOT NULL,
        fact TEXT NOT NULL,
        importance REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # -------------------------
    # EPISODIC MEMORY
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodic_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        importance REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # -------------------------
    # SUMMARY MEMORY
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summary_memory (
        id INTEGER PRIMARY KEY,
        summary TEXT
    )
    """)


    # -------------------------
    # CONVERSATION BUFFER
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_buffer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # -------------------------
    # REFLECTION MEMORY
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reflection_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson TEXT NOT NULL,
        importance REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # -------------------------
    # CHARACTER MEMORY
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS character_memory (
        trait TEXT PRIMARY KEY,
        value REAL NOT NULL
    )
    """)


    connection.commit()

    connection.close()