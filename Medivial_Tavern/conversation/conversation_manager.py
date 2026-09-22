from conversation.conversation_state import ConversationState

import random


class ConversationManager:

    def __init__(
        self,
        reviewer,
        tts_manager
    ):
        self.reviewer = reviewer
        self.tts_manager = tts_manager

        # Keeps track of conversations currently active
        self.active_conversations = []

    # ==================================================
    # REGISTER CONVERSATION
    # ==================================================

    def register_conversation(self, conversation):

        if conversation not in self.active_conversations:
            self.active_conversations.append(
                conversation
            )

    # ==================================================
    # UNREGISTER CONVERSATION
    # ==================================================

    def unregister_conversation(self, conversation):

        if conversation in self.active_conversations:
            self.active_conversations.remove(
                conversation
            )

    # ==================================================
    # NPC SPEAKS
    # ==================================================

    def speak_as(
        self,
        speaker,
        target,
        conversation,
        world_state
    ):

        history = conversation.get_history()

        response = speaker.speak(
            target=target.name,
            conversation=history,
            world_state=world_state.to_dict()
        )

        if not response:
            return None

        # Add NPC message to conversation history
        conversation.add_message(
            speaker=speaker.name,
            message=response
        )

        print(
            f"\n🗣️ {speaker.name}: {response}"
        )

        # TTS
        self._speak_tts(
            character_name=speaker.name,
            text=response
        )

        # Remember conversation
        speaker.remember_episode(
            f"Conversation with {target.name}: {response}",
            importance=0.6
        )

        return response

    # ==================================================
    # TTS
    # ==================================================

    def _speak_tts(
        self,
        character_name,
        text
    ):

        try:

            self.tts_manager.speak(
                character_name=character_name,
                text=text
            )

        except Exception as e:

            print(
                f"⚠️ TTS error: {e}"
            )

    # ==================================================
    # NPC INTERRUPTION
    # ==================================================

    def process_interruption(
        self,
        npc,
        decision,
        conversation,
        world_state
    ):

        print(
            f"\n⚡ {npc.name} interrupts the conversation!"
        )

        message = decision.message

        # ----------------------------------------------
        # If DecisionAgent did not provide a message,
        # generate one using the NPC
        # ----------------------------------------------

        if not message:

            participants = conversation.participants

            possible_targets = [
                participant
                for participant in participants
                if participant != npc
            ]

            if not possible_targets:
                return

            target = random.choice(
                possible_targets
            )

            message = npc.speak(
                target=target.name,
                conversation=conversation.get_history(),
                world_state=world_state.to_dict()
            )

        # ----------------------------------------------
        # Add interruption to conversation
        # ----------------------------------------------

        conversation.add_message(
            speaker=npc.name,
            message=message,
            forced=True
        )

        print(
            f"\n🗣️ {npc.name}: {message}"
        )

        # TTS
        self._speak_tts(
            character_name=npc.name,
            text=message
        )

        # Remember interruption
        npc.remember_episode(
            f"Interrupted a conversation: {message}",
            importance=0.7
        )

        # Add interrupter to conversation
        conversation.add_participant(
            npc
        )

    # ==================================================
    # TRAVELER SPEAKS
    # ==================================================

    def traveler_speaks(
        self,
        traveler,
        message,
        conversation,
        world_state,
        npcs
    ):

        print(
            f"\n🎒 Traveler: {message}"
        )

        # ----------------------------------------------
        # Determine who should respond
        # ----------------------------------------------

        participants = conversation.participants

        # If nobody is currently participating,
        # choose any NPC.
        if not participants:

            participants = list(
                npcs.values()
            )

        target_npc = None

        message_lower = message.lower()

        # ----------------------------------------------
        # If Traveler directly mentions an NPC,
        # that NPC gets priority.
        # ----------------------------------------------

        for npc in npcs.values():

            if npc.name.lower() in message_lower:

                target_npc = npc
                break

        # ----------------------------------------------
        # Otherwise choose someone already in the
        # conversation.
        # ----------------------------------------------

        if target_npc is None:

            if participants:

                target_npc = random.choice(
                    participants
                )

            else:

                target_npc = random.choice(
                    list(npcs.values())
                )

        # ----------------------------------------------
        # ADD TRAVELER MESSAGE
        #
        # IMPORTANT:
        # This happens ONLY ONCE.
        # ----------------------------------------------

        conversation.add_message(
            speaker=traveler.name,
            message=message,
            forced=True
        )

        # ----------------------------------------------
        # Add NPC to conversation
        # ----------------------------------------------

        conversation.add_participant(
            target_npc
        )

        # ----------------------------------------------
        # NPC responds
        # ----------------------------------------------

        response = target_npc.speak(
            target=traveler.name,
            conversation=conversation.get_history(),
            world_state=world_state.to_dict()
        )

        # ----------------------------------------------
        # Store NPC response
        # ----------------------------------------------

        if response:

            conversation.add_message(
                speaker=target_npc.name,
                message=response
            )

            print(
                f"\n🗣️ {target_npc.name}: {response}"
            )

            # TTS
            self._speak_tts(
                character_name=target_npc.name,
                text=response
            )

            # Remember interaction with Traveler
            target_npc.remember_episode(
                (
                    f"Conversation with Traveler: "
                    f"{message} -> {response}"
                ),
                importance=0.8
            )

        return response

    # ==================================================
    # START NPC CONVERSATION
    # ==================================================

    def start_conversation(
        self,
        npc_one,
        npc_two,
        world_state,
        all_npcs,
        max_turns=10
    ):

        conversation = ConversationState(
            participants=[
                npc_one,
                npc_two
            ]
        )

        # Register active conversation
        self.register_conversation(
            conversation
        )

        print(
            f"\n💬 {npc_one.name} starts talking "
            f"to {npc_two.name}"
        )

        current_speaker = npc_one

        # ==================================================
        # CONVERSATION LOOP
        # ==================================================

        for turn in range(max_turns):

            if not conversation.is_active():
                break

            print(
                f"\n──────── TURN {turn + 1} ────────"
            )

            # ------------------------------------------
            # CHECK NPC INTERRUPTIONS
            # ------------------------------------------

            interrupter, decision = (
                self.check_for_interruptions(
                    conversation=conversation,
                    all_npcs=all_npcs,
                    world_state=world_state
                )
            )

            if interrupter:

                self.process_interruption(
                    npc=interrupter,
                    decision=decision,
                    conversation=conversation,
                    world_state=world_state
                )

                # After an interruption, one of the
                # existing participants responds.
                responders = [
                    npc
                    for npc in conversation.participants
                    if npc != interrupter
                ]

                if responders:

                    current_speaker = random.choice(
                        responders
                    )

                continue

            # ------------------------------------------
            # FIND POSSIBLE TARGETS
            # ------------------------------------------

            possible_targets = [
                npc
                for npc in conversation.participants
                if npc != current_speaker
            ]

            if not possible_targets:
                break

            target = random.choice(
                possible_targets
            )

            # ------------------------------------------
            # NPC SPEAKS
            # ------------------------------------------

            self.speak_as(
                speaker=current_speaker,
                target=target,
                conversation=conversation,
                world_state=world_state
            )

            # ------------------------------------------
            # REVIEW CONVERSATION
            # ------------------------------------------

            review = self.reviewer.review(
                conversation.get_history()
            )

            if review.get(
                "should_end",
                False
            ):

                print(
                    "\n🔚 Conversation naturally ends."
                )

                break

            # ------------------------------------------
            # CHOOSE NEXT SPEAKER
            # ------------------------------------------

            next_speaker = (
                self.choose_next_speaker(
                    current_speaker=current_speaker,
                    conversation=conversation
                )
            )

            if next_speaker is None:
                break

            current_speaker = next_speaker

        # ==================================================
        # END CONVERSATION
        # ==================================================

        conversation.end()

        self.unregister_conversation(
            conversation
        )

        return conversation

    # ==================================================
    # CHECK FOR NPC INTERRUPTIONS
    # ==================================================

    def check_for_interruptions(
        self,
        conversation,
        all_npcs,
        world_state
    ):

        active_npcs = conversation.participants

        # NPCs currently outside conversation
        observers = [
            npc
            for npc in all_npcs.values()
            if npc not in active_npcs
        ]

        random.shuffle(
            observers
        )

        # Ask each observer if they want to interrupt
        for npc in observers:

            decision = npc.decide(
                world_state=world_state.to_dict(),
                characters=all_npcs,
                active_conversation=conversation.get_history()
            )

            if decision.action == "interrupt":

                return npc, decision

        return None, None

    # ==================================================
    # CHOOSE NEXT SPEAKER
    # ==================================================

    def choose_next_speaker(
        self,
        current_speaker,
        conversation
    ):

        candidates = [
            npc
            for npc in conversation.participants
            if npc != current_speaker
        ]

        if not candidates:
            return None

        return random.choice(
            candidates
        )