from config import llm


class SummaryMemory:

    def __init__(self):

        self.summary = ""

        self.recent_messages = []

        self.max_messages = 10


    def add_message(
        self,
        role: str,
        content: str
    ):

        self.recent_messages.append({
            "role": role,
            "content": content
        })


    def should_summarize(self):

        return len(self.recent_messages) > self.max_messages


    def update_summary(self):

        conversation = "\n".join(

            f"{message['role']}: {message['content']}"

            for message in self.recent_messages
        )

        prompt = f"""
You maintain a long-term conversation summary.

Existing summary:

{self.summary}

New conversation:

{conversation}

Create an updated summary.

Keep:

- Important facts
- User goals
- Important ongoing tasks
- Decisions
- Context needed for future conversations

Do not include unnecessary details.
"""

        result = llm.invoke(prompt)

        self.summary = result.content

        self.recent_messages = []


    def get_context(self):

        return {
            "summary": self.summary,
            "recent_messages": self.recent_messages
        }