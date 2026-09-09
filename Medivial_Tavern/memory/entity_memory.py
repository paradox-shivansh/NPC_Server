from database.database import (
    get_connection,
    initialize_database
)


class EntityMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id

        initialize_database(
            npc_id
        )


    def add_memory(
        self,
        entity,
        fact,
        importance=0.5
    ):

        connection = get_connection(
            self.npc_id
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO entities
            (entity, fact, importance)
            VALUES (?, ?, ?)
        """, (
            entity,
            fact,
            importance
        ))

        connection.commit()
        connection.close()


    def retrieve(
        self,
        entity=None,
        limit=10
    ):

        connection = get_connection(
            self.npc_id
        )

        cursor = connection.cursor()

        if entity:

            cursor.execute("""
                SELECT *
                FROM entities
                WHERE entity = ?
                ORDER BY importance DESC
                LIMIT ?
            """, (
                entity,
                limit
            ))

        else:

            cursor.execute("""
                SELECT *
                FROM entities
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