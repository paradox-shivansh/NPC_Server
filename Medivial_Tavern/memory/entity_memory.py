from database.database import get_connection


class EntityMemory:

    def add_memory(
        self,
        entity: str,
        fact: str,
        importance: float
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO entity_memory (
            entity,
            fact,
            importance
        )
        VALUES (?, ?, ?)
        """, (
            entity,
            fact,
            importance
        ))

        connection.commit()

        connection.close()


    def get_all(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        SELECT entity, fact, importance
        FROM entity_memory
        ORDER BY importance DESC
        """)

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]