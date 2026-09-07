from database.database import get_connection


class EpisodicMemory:

    def add_episode(
        self,
        content: str,
        importance: float
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO episodic_memory (
            content,
            importance
        )
        VALUES (?, ?)
        """, (
            content,
            importance
        ))

        connection.commit()

        connection.close()


    def get_relevant_episodes(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        SELECT content, importance, created_at
        FROM episodic_memory
        ORDER BY importance DESC, created_at DESC
        LIMIT 10
        """)

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]