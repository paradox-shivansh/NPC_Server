import random

from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    DAY_DURATION,
    SIMULATION_STEP
)

from characters.eva import create_eva
from characters.freddy import create_freddy
from characters.john import create_john

from agents.reviewer_agent import ReviewerAgent

from agents.god_agent import create_day

from conversation.conversation_manager import (
    ConversationManager
)

from world.day_manager import DayManager

from graphs.simulation_graph import (
    build_simulation_graph
)

from tts.tts_manager import TTSManager

from traveler.traveler import Traveler

from events.event_queue import (
    PlayerEventQueue
)

from input.player_input import (
    PlayerInput
)


# ======================================================
# LLM
# ======================================================

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE
)


# ======================================================
# NPCs
# ======================================================

eva = create_eva(llm)

freddy = create_freddy(llm)

john = create_john(llm)


characters = {
    "Eva": eva,
    "Freddy": freddy,
    "John": john
}


# ======================================================
# TRAVELER
# ======================================================

traveler = Traveler()


# ======================================================
# REVIEWER
# ======================================================

reviewer = ReviewerAgent(
    llm
)


# ======================================================
# TTS
# ======================================================

tts_manager = TTSManager()


# ======================================================
# CONVERSATION MANAGER
# ======================================================

conversation_manager = ConversationManager(
    reviewer=reviewer,
    tts_manager=tts_manager
)


# ======================================================
# PLAYER EVENTS
# ======================================================

player_event_queue = PlayerEventQueue()


player_input = PlayerInput(
    event_queue=player_event_queue
)


# ======================================================
# CURRENT PLAYER CONVERSATION
# ======================================================

player_conversation = None


# ======================================================
# WORLD
# ======================================================

def generate_day(day_number):

    return create_day(
        llm=llm,
        day_number=day_number
    )


# ======================================================
# PROCESS PLAYER EVENTS
# ======================================================

def process_player_events(world):

    global player_conversation

    while player_event_queue.has_events():

        event = player_event_queue.get()

        if event is None:
            return False

        # ----------------------------------------------
        # QUIT
        # ----------------------------------------------

        if event.event_type == "quit":

            print(
                "\n🛑 Traveler requested shutdown."
            )

            return True

        # ----------------------------------------------
        # SPEAK
        # ----------------------------------------------

        if event.event_type == "speak":

            # Create a new Traveler conversation
            # if none exists.

            if player_conversation is None:

                target = random.choice(
                    list(characters.values())
                )

                from conversation.conversation_state import (
                    ConversationState
                )

                player_conversation = (
                    ConversationState(
                        participants=[
                            target
                        ]
                    )
                )

                conversation_manager.register_conversation(
                    player_conversation
                )

            conversation_manager.traveler_speaks(
                traveler=traveler,
                message=event.message,
                conversation=player_conversation,
                world_state=world,
                npcs=characters
            )

    return False


# ======================================================
# NPC SIMULATION
# ======================================================

def run_simulation(world):

    # ----------------------------------------------
    # FIRST: HANDLE TRAVELER
    # ----------------------------------------------

    should_stop = process_player_events(
        world
    )

    if should_stop:
        raise KeyboardInterrupt


    # ----------------------------------------------
    # NPC DECISION
    # ----------------------------------------------

    npc = random.choice(
        list(characters.values())
    )

    decision = npc.decide(
        world_state=world.to_dict(),
        characters=characters
    )

    print(
        f"\n🎭 {npc.name} decided:"
    )

    print(
        decision
    )

    # ----------------------------------------------
    # TALK
    # ----------------------------------------------

    if decision.action != "talk":

        print(
            f"{npc.name} chooses to "
            f"{decision.action}."
        )

        return

    # ----------------------------------------------
    # TARGET
    # ----------------------------------------------

    target_name = decision.target

    if not target_name:

        print(
            f"⚠️ {npc.name} chose to talk "
            f"but did not select a target."
        )

        return

    target = None

    for character in characters.values():

        if (
            character.name.lower()
            == target_name.lower()
        ):

            target = character
            break

    if target is None:

        print(
            f"⚠️ Target '{target_name}' "
            f"not found."
        )

        return

    if target.name == npc.name:

        print(
            f"⚠️ {npc.name} cannot "
            f"talk to themselves."
        )

        return

    # ----------------------------------------------
    # START CONVERSATION
    # ----------------------------------------------

    print(
        f"\n💬 {npc.name} wants to talk "
        f"to {target.name}"
    )

    conversation_manager.start_conversation(
        npc_one=npc,
        npc_two=target,
        world_state=world,
        all_npcs=characters
    )


# ======================================================
# DAY MANAGER
# ======================================================

day_manager = DayManager(
    duration=DAY_DURATION,
    simulation_step=SIMULATION_STEP
)


# ======================================================
# SIMULATION GRAPH
# ======================================================

simulation_graph = build_simulation_graph(
    create_day_function=generate_day,
    run_simulation_function=lambda world:
        day_manager.run_day(
            run_simulation,
            world
        )
)


# ======================================================
# START
# ======================================================

print(
    "\n🧙 MEDIEVAL TAVERN SIMULATION"
)

print(
    "Eva, Freddy and John are alive."
)

print(
    "Traveler has entered the tavern."
)

print(
    "You can speak at any time."
)

print(
    "Type 'quit' to stop.\n"
)


# ======================================================
# START INPUT THREAD
# ======================================================

player_input.start()


# ======================================================
# DAYS
# ======================================================

day_number = 1


try:

    while True:

        print(
            f"\n\n🌅 STARTING DAY {day_number}"
        )

        simulation_graph.invoke(
            {
                "day_number": day_number,
                "world": None
            }
        )

        day_number += 1


except KeyboardInterrupt:

    print(
        "\n\n🛑 Simulation stopped."
    )

    print(
        "Persistent memories remain stored."
    )

finally:

    player_input.stop()