from langchain_core.prompts import ChatPromptTemplate

from schemas.decisions import NPCDecision


def decide_action(

    llm,

    npc_name,

    personality,

    mood,

    world_state,

    available_characters

):


    structured_llm = llm.with_structured_output(

        NPCDecision

    )


    prompt = ChatPromptTemplate.from_template(

        """
You are controlling an autonomous NPC.

NPC:

{npc_name}

PERSONALITY:

{personality}

CURRENT MOOD:

{mood}

WORLD:

{world_state}

AVAILABLE CHARACTERS:

{available_characters}

Decide what the NPC naturally wants to do.

Possible actions:

talk
wait
interrupt
leave

Do not force conversation.

Choose an action naturally based on personality and mood.
"""
    )


    chain = prompt | structured_llm


    return chain.invoke({

        "npc_name": npc_name,

        "personality": personality,

        "mood": mood,

        "world_state": world_state,

        "available_characters": available_characters

    })