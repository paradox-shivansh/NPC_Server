import json

from database.database import (
    get_connection,
    initialize_database
)


class CharacterMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id

        initialize_database(
            npc_id
        )


    def update_traits(
        self,
        traits
    ):

        connection = get_connection(
            self.npc_id
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO character_memory
            (traits)
            VALUES (?)
        """, (
            json.dumps(traits),
        ))

        connection.commit()
        connection.close()


    def get_traits(self):

        connection = get_connection(
            self.npc_id
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT traits
            FROM character_memory
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        connection.close()

        if row:

            return json.loads(
                row["traits"]
            )

        return {}