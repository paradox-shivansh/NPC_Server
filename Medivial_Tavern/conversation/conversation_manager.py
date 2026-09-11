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
    # CHECK WHETHER AN OUTSIDE NPC WANTS TO INTERRUPT
    # =====================================================

    def check_for_interruptions(
        self,
        conversation,
        all_npcs,
        world_state
    ):

        # NPCs already inside the conversation
        active_npcs = conversation.participants

        # NPCs who are currently outside
        observers = [
            npc
            for npc in all_npcs.values()
            if npc not in active_npcs
        ]

        # Ask each outside NPC whether they want
        # to interrupt / join
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

        # -----------------------------------------
        # GET INTERRUPTION MESSAGE
        # -----------------------------------------

        message = decision.message

        # If the decision agent didn't provide one,
        # generate one normally
        if not message:

            target = decision.target or "everyone"

            message = npc.speak(
                target=target,
                conversation=conversation.get_history(),
                world_state=world_state.to_dict()
            )

        # -----------------------------------------
        # PRINT
        # -----------------------------------------

        print(
            f"\n{npc.name}: {message}"
        )

        # -----------------------------------------
        # SAVE MESSAGE
        # -----------------------------------------

        conversation.add_message(
            npc.name,
            message
        )

        # -----------------------------------------
        # TTS
        # -----------------------------------------

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

        # -----------------------------------------
        # ADD NPC TO CONVERSATION
        # -----------------------------------------

        conversation.add_participant(
            npc
        )

        # -----------------------------------------
        # MEMORY
        # -----------------------------------------

        npc.remember_episode(
            f"Interrupted a conversation: {message}",
            importance=0.7
        )

        return decision

    # =====================================================
    # CHOOSE NEXT SPEAKER
    # =====================================================

    def choose_next_speaker(
        self,
        current_speaker,
        conversation
    ):

        participants = conversation.participants

        # Nobody else is available
        if len(participants) <= 1:
            return None

        possible_speakers = [
            npc
            for npc in participants
            if npc != current_speaker
        ]

        return random.choice(
            possible_speakers
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

        # -----------------------------------------
        # CREATE CONVERSATION
        # -----------------------------------------

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

        # First speaker
        current_speaker = npc_one

        # -----------------------------------------
        # CONVERSATION LOOP
        # -----------------------------------------

        for turn in range(10):

            print(
                f"\n──────── TURN {turn + 1} ────────"
            )

            # =================================================
            # CHECK FOR OUTSIDE NPC INTERRUPTION
            # =================================================

            interrupter, decision = (
                self.check_for_interruptions(
                    conversation=conversation,
                    all_npcs=all_npcs,
                    world_state=world_state
                )
            )

            # -----------------------------------------
            # INTERRUPTION FOUND
            # -----------------------------------------

            if interrupter:

                self.process_interruption(
                    npc=interrupter,
                    decision=decision,
                    conversation=conversation,
                    world_state=world_state
                )

                # The interrupter gets a chance to
                # continue the conversation
                current_speaker = interrupter

                continue

            # =================================================
            # CHOOSE WHO CURRENT NPC IS TALKING TO
            # =================================================

            possible_targets = [
                npc
                for npc in conversation.participants
                if npc != current_speaker
            ]

            if not possible_targets:

                print(
                    "\n🔚 No other participants."
                )

                break

            target = random.choice(
                possible_targets
            )

            # =================================================
            # GET HISTORY
            # =================================================

            history = conversation.get_history()

            # =================================================
            # GENERATE RESPONSE
            # =================================================

            response = current_speaker.speak(
                target=target.name,
                conversation=history,
                world_state=world_state.to_dict()
            )

            # =================================================
            # SAVE MESSAGE
            # =================================================

            conversation.add_message(
                current_speaker.name,
                response
            )

            # =================================================
            # PRINT
            # =================================================

            print(
                f"\n{current_speaker.name}: "
                f"{response}"
            )

            # =================================================
            # TTS
            # =================================================

            if response and response.strip():

                try:

                    self.tts_manager.speak(
                        character_name=current_speaker.name,
                        text=response
                    )

                except Exception as e:

                    print(
                        f"⚠️ TTS error: {e}"
                    )

                    print(
                        "Continuing conversation..."
                    )

            # =================================================
            # MEMORY
            # =================================================

            current_speaker.remember_episode(
                f"Conversation with "
                f"{target.name}: {response}",
                importance=0.6
            )

            # =================================================
            # REVIEW CONVERSATION
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
            # CHOOSE NEXT SPEAKER
            # =================================================

            next_speaker = self.choose_next_speaker(
                current_speaker=current_speaker,
                conversation=conversation
            )

            if next_speaker is None:

                print(
                    "\n🔚 Conversation has no next speaker."
                )

                break

            current_speaker = next_speaker

        return conversation