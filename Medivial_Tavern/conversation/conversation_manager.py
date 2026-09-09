from conversation.conversation_state import (
    ConversationState
)


class ConversationManager:

    def __init__(
        self,
        reviewer
    ):

        self.reviewer = reviewer


    def start_conversation(
        self,
        npc_one,
        npc_two,
        world_state
    ):

        conversation = ConversationState(
            participants=[
                npc_one,
                npc_two
            ]
        )

        print(
            f"\n💬 {npc_one.name} "
            f"starts talking to "
            f"{npc_two.name}"
        )

        current_speaker = npc_one

        for _ in range(8):

            target = (
                npc_two
                if current_speaker == npc_one
                else npc_one
            )

            history = conversation.get_history()

            response = current_speaker.speak(
                target=target.name,
                conversation=history,
                world_state=world_state.to_dict()
            )

            conversation.add_message(
                current_speaker.name,
                response
            )

            print(
                f"\n{current_speaker.name}: "
                f"{response}"
            )

            # BOTH NPCs remember the event
            current_speaker.remember_episode(
                f"""
                Conversation with {target.name}.
                {current_speaker.name} said:
                {response}
                """,
                importance=0.6
            )

            target.remember_episode(
                f"""
                Conversation with {current_speaker.name}.
                {current_speaker.name} said:
                {response}
                """,
                importance=0.6
            )

            review = self.reviewer.review(
                conversation.get_history()
            )

            if review["should_end"]:

                print(
                    "\n🔚 Conversation naturally ends."
                )

                break

            current_speaker = target

        return conversation