from agents.npc_agent import NPCAgent


def create_freddy(llm):

    config = {
        "name": "Freddy",
        "role": "Tavern owner",

        "personality": (
            "Freddy is a man in his early 50s and a family man. "
            "He is hardworking, responsible and cares deeply about "
            "his family and his tavern. Recently he has become "
            "frustrated and short-tempered because the tavern is "
            "losing money. He can be grumpy when stressed, but he "
            "is not a bad person."
        ),

        "mood": "frustrated"
    }

    return NPCAgent(
        npc_id="freddy",
        name=config["name"],
        role=config["role"],
        personality=config["personality"],
        mood=config["mood"],
        llm=llm
    )