class ConversationState:

    def __init__(
        self,
        participants
    ):

        self.participants = participants

        self.messages = []


    def add_message(
        self,
        speaker,
        content
    ):

        self.messages.append({
            "speaker": speaker,
            "content": content
        })


    def get_history(self):

        return "\n".join(
            f"{message['speaker']}: "
            f"{message['content']}"

            for message
            in self.messages
        )