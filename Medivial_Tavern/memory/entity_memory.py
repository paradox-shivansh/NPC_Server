from database.database import get_connection


class EntityMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id

        self.create_table()


    def create_table(self):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entity_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            entity TEXT,

            fact TEXT,

            importance REAL,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """)

        connection.commit()

        connection.close()


    def add_memory(

        self,

        entity,

        fact,

        importance=0.5

    ):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO entity_memory

        (entity, fact, importance)

        VALUES (?, ?, ?)
        """, (

            entity,

            fact,

            importance

        ))

        connection.commit()

        connection.close()


    def search_memory(

        self,

        query,

        limit=5

    ):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        SELECT *

        FROM entity_memory

        WHERE entity LIKE ?
        OR fact LIKE ?

        ORDER BY importance DESC

        LIMIT ?
        """, (

            f"%{query}%",

            f"%{query}%",

            limit

        ))

        rows = cursor.fetchall()

        connection.close()

        return [

            dict(row)

            for row in rows

        ]