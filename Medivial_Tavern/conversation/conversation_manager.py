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

    # =====================================================
    # SPEAK + TTS + MEMORY
    # =====================================================

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

        # -------------------------------------------------
        # SAVE MESSAGE
        # -------------------------------------------------

        conversation.add_message(
            speaker.name,
            response
        )

        # -------------------------------------------------
        # PRINT
        # -------------------------------------------------

        print(
            f"\n{speaker.name}: {response}"
        )

        # -------------------------------------------------
        # TTS
        # -------------------------------------------------

        if response and response.strip():

            try:

                self.tts_manager.speak(
                    character_name=speaker.name,
                    text=response
                )

            except Exception as e:

                print(
                    f"⚠️ TTS error: {e}"
                )

        # -------------------------------------------------
        # MEMORY
        # -------------------------------------------------

        speaker.remember_episode(
            f"Conversation with "
            f"{target.name}: {response}",
            importance=0.6
        )

        return response

    # =====================================================
    # CHECK FOR INTERRUPTIONS
    # =====================================================

    def check_for_interruptions(
        self,
        conversation,
        all_npcs,
        world_state
    ):

        active_npcs = conversation.participants

        observers = [
            npc
            for npc in all_npcs.values()
            if npc not in active_npcs
        ]

        # Randomize observer order so the same NPC
        # does not always get priority.
        random.shuffle(observers)

        for npc in observers:

            decision = npc.decide(
                world_state=world_state.to_dict(),
                characters=all_npcs,
                active_conversation=conversation.get_history()
            )

            if decision.action == "interrupt":

                return npc, decision

        return None, None

    # =====================================================
    # PROCESS INTERRUPTION
    # =====================================================

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

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        message = decision.message

        # If the LLM did not provide a message,
        # generate one.
        if not message:

            participants = conversation.participants

            target = random.choice(
                [
                    p
                    for p in participants
                    if p != npc
                ]
            )

            message = npc.speak(
                target=target.name,
                conversation=conversation.get_history(),
                world_state=world_state.to_dict()
            )

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        conversation.add_message(
            npc.name,
            message
        )

        # -------------------------------------------------
        # PRINT
        # -------------------------------------------------

        print(
            f"\n{npc.name}: {message}"
        )

        # -------------------------------------------------
        # TTS
        # -------------------------------------------------

        if message and message.strip():

            try:

                self.tts_manager.speak(
                    character_name=npc.name,
                    text=message
                )

            except Exception as e:

                print(
                    f"⚠️ TTS error: {e}"
                )

        # -------------------------------------------------
        # MEMORY
        # -------------------------------------------------

        npc.remember_episode(
            f"Interrupted a conversation: {message}",
            importance=0.7
        )

        # -------------------------------------------------
        # ADD NPC
        # -------------------------------------------------

        conversation.add_participant(
            npc
        )

        return npc

    # =====================================================
    # CHOOSE NEXT SPEAKER
    # =====================================================

    def choose_next_speaker(
        self,
        current_speaker,
        conversation
    ):

        participants = conversation.participants

        candidates = [
            npc
            for npc in participants
            if npc != current_speaker
        ]

        if not candidates:
            return None

        return random.choice(
            candidates
        )

    # =====================================================
    # START CONVERSATION
    # =====================================================

    def start_conversation(
        self,
        npc_one,
        npc_two,
        world_state,
        all_npcs
    ):

        conversation = ConversationState(
            participants=[
                npc_one,
                npc_two
            ]
        )

        print(
            f"\n💬 {npc_one.name} starts talking "
            f"to {npc_two.name}"
        )

        current_speaker = npc_one

        # =================================================
        # CONVERSATION LOOP
        # =================================================

        for turn in range(10):

            print(
                f"\n──────── TURN {turn + 1} ────────"
            )

            # =================================================
            # CHECK FOR OUTSIDE INTERRUPTIONS
            # =================================================

            interrupter, decision = (
                self.check_for_interruptions(
                    conversation=conversation,
                    all_npcs=all_npcs,
                    world_state=world_state
                )
            )

            # =================================================
            # INTERRUPTION
            # =================================================

            if interrupter:

                self.process_interruption(
                    npc=interrupter,
                    decision=decision,
                    conversation=conversation,
                    world_state=world_state
                )

                # -----------------------------------------
                # IMPORTANT
                #
                # The interrupter has already spoken.
                #
                # DO NOT set:
                #
                # current_speaker = interrupter
                #
                # Instead choose an existing participant
                # to respond.
                # -----------------------------------------

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

            # =================================================
            # CHOOSE TARGET
            # =================================================

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

            # =================================================
            # NPC SPEAKS
            # =================================================

            self.speak_as(
                speaker=current_speaker,
                target=target,
                conversation=conversation,
                world_state=world_state
            )

            # =================================================
            # REVIEW
            # =================================================

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

            # =================================================
            # NEXT SPEAKER
            # =================================================

            next_speaker = (
                self.choose_next_speaker(
                    current_speaker=current_speaker,
                    conversation=conversation
                )
            )

            if next_speaker is None:

                break

            current_speaker = next_speaker

        return conversation