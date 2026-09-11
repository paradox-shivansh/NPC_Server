class ConversationState:

    def __init__(self, participants):

        self.participants = participants
        self.messages = []


    def add_participant(self, npc):

        if npc not in self.participants:

            self.participants.append(npc)


    def remove_participant(self, npc):

        if npc in self.participants:

            self.participants.remove(npc)


    def add_message(
        self,
        speaker,
        message
    ):

        self.messages.append(
            {
                "speaker": speaker,
                "message": message
            }
        )


    def get_history(self):

        return self.messages