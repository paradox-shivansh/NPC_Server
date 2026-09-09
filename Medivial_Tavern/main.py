from langchain_groq import ChatGroq


from config.settings import (

    MODEL_NAME,

    TEMPERATURE,

    DAY_DURATION,

    SIMULATION_STEP

)


from characters.eva import create_eva

from characters.freddy import create_freddy

from characters.john import create_john


from agents.god_agent import create_day

from agents.reviewer_agent import ReviewerAgent


from world.world_state import WorldState

from world.day_manager import DayManager


from conversation.conversation_manager import ConversationManager

from database.schema import initialize_database


initialize_database("eva")
initialize_database("freddy")
initialize_database("john")
# =====================================
# CREATE LLM
# =====================================

llm = ChatGroq(

    model=MODEL_NAME,

    temperature=TEMPERATURE

)


# =====================================
# CREATE NPCs
# =====================================

eva = create_eva(

    llm

)


freddy = create_freddy(

    llm

)


john = create_john(

    llm


)


characters = [

    eva,

    freddy,

    john

]


# =====================================
# REVIEWER
# =====================================

reviewer = ReviewerAgent(

    llm

)


conversation_manager = ConversationManager(

    reviewer

)


# =====================================
# DAY MANAGER
# =====================================
day_manager = DayManager(
    duration=DAY_DURATION,
    simulation_step=SIMULATION_STEP
)

# =====================================
# CREATE WORLD
# =====================================

def generate_world(

    day_number

):


    daily_world = create_day(

        llm,

        day_number

    )


    world = WorldState(

        day_number=day_number,

        weather=daily_world.weather,

        tavern_condition=daily_world.tavern_condition,

        event=daily_world.event

    )


    # Apply mood changes

    eva.mood["happiness"] += (

        daily_world.eva_mood_change

    )


    freddy.mood["happiness"] += (

        daily_world.freddy_mood_change

    )


    john.mood["happiness"] += (

        daily_world.john_mood_change

    )


    return world


# =====================================
# SIMULATION STEP
# =====================================

def simulation_step(

    world

):


    print(

        "\n"

        "============================"

    )


    print(

        "🧠 NPC DECISION PHASE"

    )


    print(

        "============================"

    )


    decisions = []


    for npc in characters:


        other_characters = [

            character.name

            for character in characters

            if character != npc

        ]


        decision = npc.decide(

            world_state=world.to_dict(),

            characters=other_characters

        )


        decisions.append(

            (

                npc,

                decision

            )

        )


        print(

            f"\n{npc.name}"

            f" → {decision.action}"

            f" → {decision.target}"

        )


    # Find someone who wants to talk

    for npc, decision in decisions:


        if (

            decision.action == "talk"

            and decision.target

        ):


            target = next(

                (

                    character

                    for character in characters

                    if character.name.lower()

                    == decision.target.lower()

                ),

                None

            )


            if target:


                conversation_manager.start_conversation(

                    npc_one=npc,

                    npc_two=target,

                    world_state=world

                )


                break


# =====================================
# MAIN SIMULATION
# =====================================

print(

    "\n🏰 MEDIEVAL TAVERN SIMULATION STARTED"

)


print(

    "Press CTRL+C to stop.\n"

)


day_number = 1


try:


    while True:


        print(

            "\n"

            "===================================="

        )


        print(

            f"🌅 DAY {day_number}"

        )


        print(

            "===================================="

        )


        world = generate_world(

            day_number

        )


        print(

            f"\n🌦 Weather: {world.weather}"

        )


        print(

            f"🏰 Tavern: {world.tavern_condition}"

        )


        print(

            f"⚡ Event: {world.event}"

        )


        day_manager.run_day(

            lambda:

            simulation_step(

                world

            )

        )


        print(

            f"\n🌙 DAY {day_number} ENDED"

        )


        day_number += 1


except KeyboardInterrupt:


    print(

        "\n\n🛑 Simulation stopped."

    )