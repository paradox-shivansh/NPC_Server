import random

from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    DAY_DURATION,
    SIMULATION_STEP,
)

from characters.eva import create_eva
from characters.freddy import create_freddy
from characters.john import create_john

from agents.reviewer_agent import ReviewerAgent
from agents.god_agent import create_day

from conversation.conversation_manager import ConversationManager

from world.day_manager import DayManager

from graphs.simulation_graph import build_simulation_graph


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
)


# --------------------------------------------------
# CHARACTERS
# --------------------------------------------------

eva = create_eva(llm)
freddy = create_freddy(llm)
john = create_john(llm)

characters = {
    "Eva": eva,
    "Freddy": freddy,
    "John": john,
}


# --------------------------------------------------
# REVIEWER
# --------------------------------------------------

reviewer = ReviewerAgent(llm)

conversation_manager = ConversationManager(
    reviewer
)


# --------------------------------------------------
# GOD
# --------------------------------------------------

def generate_day(day_number):
    return create_day(
        llm=llm,
        day_number=day_number,
    )


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation(world):

    # Random NPC gets a chance to initiate
    npc = random.choice(
        list(characters.values())
    )

    # Ask the NPC what it wants to do
    decision = npc.decide(
        world_state=world.to_dict(),
        characters=characters,
    )

    print(
        f"\n🎭 {npc.name} decided:"
    )

    print(
        decision
    )

    # --------------------------------------------------
    # NON-TALK ACTION
    # --------------------------------------------------

    if decision.action != "talk":

        print(
            f"{npc.name} chooses to "
            f"{decision.action}."
        )

        return

    # --------------------------------------------------
    # TALK ACTION
    # --------------------------------------------------

    target_name = decision.target

    if not target_name:

        print(
            f"⚠️ {npc.name} chose to talk "
            f"but did not select a target."
        )

        return

    # --------------------------------------------------
    # FIND TARGET
    # --------------------------------------------------

    target = None

    for character in characters.values():

        if (
            character.name.lower()
            == target_name.lower()
        ):
            target = character
            break

    # --------------------------------------------------
    # TARGET NOT FOUND
    # --------------------------------------------------

    if target is None:

        print(
            f"⚠️ Target '{target_name}' "
            f"not found."
        )

        return

    # Prevent self-conversation
    if target.name == npc.name:

        print(
            f"⚠️ {npc.name} cannot talk "
            f"to themselves."
        )

        return

    # --------------------------------------------------
    # START CONVERSATION
    # --------------------------------------------------

    print(
        f"\n💬 {npc.name} wants to talk "
        f"to {target.name}"
    )

    conversation_manager.start_conversation(
        npc_one=npc,
        npc_two=target,
        world_state=world,
    )


# --------------------------------------------------
# DAY MANAGER
# --------------------------------------------------

day_manager = DayManager(
    duration=DAY_DURATION,
    simulation_step=SIMULATION_STEP,
)


# --------------------------------------------------
# LANGGRAPH SIMULATION
# --------------------------------------------------

simulation_graph = build_simulation_graph(
    create_day_function=generate_day,

    run_simulation_function=lambda world:
        day_manager.run_day(
            run_simulation,
            world,
        ),
)


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

print(
    "\n🧙 MEDIEVAL TAVERN SIMULATION"
)

print(
    "Eva, Freddy and John are alive."
)

print(
    "Type Ctrl+C to stop.\n"
)


day_number = 1


try:

    while True:

        print(
            "\n================================"
        )

        print(
            f"STARTING DAY {day_number}"
        )

        print(
            "================================"
        )

        # Run one complete day
        simulation_graph.invoke(
            {
                "day_number": day_number,
                "world": None,
            }
        )

        # Move to next day
        day_number += 1


except KeyboardInterrupt:

    print(
        "\n\n🛑 Simulation stopped."
    )

    print(
        "All persistent memories remain stored."
    )