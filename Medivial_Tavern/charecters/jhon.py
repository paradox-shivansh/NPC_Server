from agents.npc_agent import NPCAgent

from config.characters import CHARACTERS


def create_john(

    llm

):


    data = CHARACTERS["john"]


    return NPCAgent(

        npc_id="john",

        name=data["name"],

        role=data["role"],

        personality=data["description"],

        mood=data["default_mood"],

        llm=llm

    )