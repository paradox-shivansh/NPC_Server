from agents.npc_agent import NPCAgent

from config.characters import CHARACTERS


def create_freddy(

    llm

):


    data = CHARACTERS["freddy"]


    return NPCAgent(

        npc_id="freddy",

        name=data["name"],

        role=data["role"],

        personality=data["description"],

        mood=data["default_mood"],

        llm=llm

    )