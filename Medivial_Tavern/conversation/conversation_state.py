class ConversationState:

    def __init__(self, participants=None):

        self.participants = participants or []

        self.messages = []

        self.active = True

    # --------------------------------------------------
    # PARTICIPANTS
    # --------------------------------------------------

    def add_participant(self, npc):

        if npc not in self.participants:
            self.participants.append(npc)

    def remove_participant(self, npc):

        if npc in self.participants:
            self.participants.remove(npc)

    # --------------------------------------------------
    # MESSAGES
    # --------------------------------------------------

    def add_message(
        self,
        speaker,
        message,
        forced=False
    ):

        self.messages.append(
            {
                "speaker": speaker,
                "message": message,
                "forced": forced
            }
        )

    def get_history(self):

        return self.messages

    # --------------------------------------------------
    # CONTROL
    # --------------------------------------------------

    def end(self):

        self.active = False

    def is_active(self):

        return self.active

    # --------------------------------------------------
    # DEBUG
    # --------------------------------------------------

    def __repr__(self):

        participants = [
            npc.name
            for npc in self.participants
        ]

        return (
            f"Conversation("
            f"participants={participants}, "
            f"messages={len(self.messages)}, "
            f"active={self.active})"
        )