from database.database import (
    get_connection,
    initialize_database
)


class ReflectionMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id

        initialize_database(
            npc_id
        )


    def add_reflection(
        self,
        lesson,
        importance=0.5
    ):

        connection = get_connection(
            self.npc_id
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO reflection_memory
            (lesson, importance)
            VALUES (?, ?)
        """, (
            lesson,
            importance
        ))

        connection.commit()
        connection.close()


    def get_reflections(
        self,
        limit=5
    ):

        connection = get_connection(
            self.npc_id
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM reflection_memory
            ORDER BY importance DESC
            LIMIT ?
        """, (
            limit,
        ))

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]