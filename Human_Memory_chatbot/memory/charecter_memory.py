from database.database import get_connection


class CharacterMemory:

    def __init__(self):

        self.initialize_traits()


    def initialize_traits(self):

        default_traits = {
            "humor": 0.5,
            "empathy": 0.7,
            "curiosity": 0.8,
            "formality": 0.5
        }

        connection = get_connection()

        cursor = connection.cursor()

        for trait, value in default_traits.items():

            cursor.execute("""
            INSERT OR IGNORE INTO character_memory (
                trait,
                value
            )
            VALUES (?, ?)
            """, (
                trait,
                value
            ))

        connection.commit()

        connection.close()


    def get_traits(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        SELECT trait, value
        FROM character_memory
        """)

        rows = cursor.fetchall()

        connection.close()

        return {
            row["trait"]: row["value"]
            for row in rows
        }


    def update_trait(
        self,
        trait: str,
        value: float
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        UPDATE character_memory
        SET value = ?
        WHERE trait = ?
        """, (
            value,
            trait
        ))

        connection.commit()

        connection.close()