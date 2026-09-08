import json

from database.database import get_connection


class RelationshipMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id

        self.create_table()


    def create_table(self):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (

            character TEXT PRIMARY KEY,

            relationship_data TEXT

        )
        """)

        connection.commit()

        connection.close()


    def get_relationship(

        self,

        character

    ):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        SELECT relationship_data

        FROM relationships

        WHERE character = ?
        """, (

            character,

        ))

        row = cursor.fetchone()

        connection.close()


        if row:

            return json.loads(

                row["relationship_data"]

            )


        return {

            "trust": 0.5,

            "affection": 0.5,

            "annoyance": 0.0

        }


    def update_relationship(

        self,

        character,

        data

    ):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO relationships

        (character, relationship_data)

        VALUES (?, ?)
        """, (

            character,

            json.dumps(data)

        ))

        connection.commit()

        connection.close()