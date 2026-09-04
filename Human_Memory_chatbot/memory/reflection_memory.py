from database.database import get_connection


class ReflectionMemory:

    def add_reflection(
        self,
        lesson: str,
        importance: float
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO reflection_memory (
            lesson,
            importance
        )
        VALUES (?, ?)
        """, (
            lesson,
            importance
        ))

        connection.commit()

        connection.close()


    def get_reflections(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        SELECT lesson, importance, created_at
        FROM reflection_memory
        ORDER BY importance DESC
        LIMIT 10
        """)

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]