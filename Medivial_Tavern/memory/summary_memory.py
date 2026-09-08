from database.database import get_connection


class SummaryMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id

        self.create_table()


    def create_table(self):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS summary_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            summary TEXT,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """)

        connection.commit()

        connection.close()


    def update_summary(

        self,

        summary

    ):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO summary_memory

        (summary)

        VALUES (?)
        """, (

            summary,

        ))

        connection.commit()

        connection.close()


    def get_latest(

        self

    ):

        connection = get_connection(self.npc_id)

        cursor = connection.cursor()

        cursor.execute("""
        SELECT summary

        FROM summary_memory

        ORDER BY id DESC

        LIMIT 1
        """)

        row = cursor.fetchone()

        connection.close()


        if row:

            return row["summary"]


        return ""