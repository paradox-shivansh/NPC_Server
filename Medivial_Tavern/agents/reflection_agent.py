import json


def generate_reflection(
    llm,
    npc,
    conversation
):

    prompt = f"""
You are the internal reflection system
for the NPC {npc.name}.

PERSONALITY:
{npc.personality}

CONVERSATION:
{conversation}

Determine what {npc.name} learned from this interaction.

Return ONLY JSON:

{{
    "lesson": "what the character learned",
    "importance": 0.0
}}

Importance must be between 0 and 1.
"""

    response = llm.invoke(
        prompt
    )

    try:

        return json.loads(
            response.content
        )

    except Exception:

        return {
            "lesson": "",
            "importance": 0
        }