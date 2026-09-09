from conversation.conversation_state import ConversationState


class ConversationManager:

    def __init__(self, reviewer, tts_manager):

        self.reviewer = reviewer
        self.tts_manager = tts_manager


    def start_conversation(
        self,
        npc_one,
        npc_two,
        world_state,
    ):

        conversation = ConversationState(
            participants=[
                npc_one,
                npc_two,
            ]
        )

        print(
            f"\n💬 {npc_one.name} starts talking "
            f"to {npc_two.name}"
        )

        current_speaker = npc_one

        for _ in range(6):

            # -----------------------------------------
            # DETERMINE OTHER PARTICIPANT
            # -----------------------------------------

            target = (
                npc_two
                if current_speaker == npc_one
                else npc_one
            )


            # -----------------------------------------
            # GET CONVERSATION HISTORY
            # -----------------------------------------

            history = conversation.get_history()


            # -----------------------------------------
            # GENERATE NPC RESPONSE
            # -----------------------------------------

            response = current_speaker.speak(
                target=target.name,
                conversation=history,
                world_state=world_state.to_dict(),
            )


            # -----------------------------------------
            # SAVE MESSAGE
            # -----------------------------------------

            conversation.add_message(
                current_speaker.name,
                response,
            )


            # -----------------------------------------
            # PRINT
            # -----------------------------------------

            print(
                f"\n{current_speaker.name}: "
                f"{response}"
            )


            # -----------------------------------------
            # 🔊 TEXT TO SPEECH
            # -----------------------------------------

            if response and response.strip():

                try:

                    self.tts_manager.speak(
                        character_name=current_speaker.name,
                        text=response,
                    )

                except Exception as e:

                    print(
                        f"⚠️ TTS error: {e}"
                    )

                    print(
                        "Continuing conversation..."
                    )


            # -----------------------------------------
            # SAVE MEMORY
            # -----------------------------------------

            current_speaker.remember_episode(
                f"Conversation with "
                f"{target.name}: {response}",
                importance=0.6,
            )


            # -----------------------------------------
            # REVIEW CONVERSATION
            # -----------------------------------------

            review = self.reviewer.review(
                conversation.get_history()
            )

            if review.get("should_end", False):
                print(
                    "\n🔚 Conversation naturally ends."
                )
                break

            # -----------------------------------------
            # SWITCH SPEAKER
            # -----------------------------------------

            current_speaker = target


        return conversation