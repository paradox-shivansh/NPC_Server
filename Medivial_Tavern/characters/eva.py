from agents.npc_agent import NPCAgent

from config.characters import CHARACTERS


def create_eva(

    llm

):


    data = CHARACTERS["eva"]


    return NPCAgent(

        npc_id="eva",

        name=data["name"],

        role=data["role"],

        personality=data["description"],

        mood=data["default_mood"],

        llm=llm

    )