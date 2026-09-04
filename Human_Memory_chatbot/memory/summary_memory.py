from database.database import get_connection


class SummaryMemory:

    def add_message(
        self,
        role: str,
        content: str
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO conversation_buffer (
            role,
            content
        )
        VALUES (?, ?)
        """, (
            role,
            content
        ))

        connection.commit()

        connection.close()


    def get_context(self):

        connection = get_connection()

        cursor = connection.cursor()


        # Get summary

        cursor.execute("""
        SELECT summary
        FROM summary_memory
        WHERE id = 1
        """)

        row = cursor.fetchone()

        summary = ""

        if row:
            summary = row["summary"] or ""


        # Get recent messages

        cursor.execute("""
        SELECT role, content
        FROM conversation_buffer
        ORDER BY id DESC
        LIMIT 10
        """)

        messages = cursor.fetchall()

        connection.close()


        messages = list(reversed(messages))


        return {
            "summary": summary,
            "recent_messages": [
                dict(message)
                for message in messages
            ]
        }


    def should_summarize(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM conversation_buffer
        """)

        count = cursor.fetchone()[0]

        connection.close()

        return count >= 20


    def update_summary(self):

        # We will connect this
        # to your LLM summarization agent next

        pass