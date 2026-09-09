import json

from world.world_state import WorldState


def create_day(
    llm,
    day_number
):

    prompt = f"""
You are the God entity controlling a medieval tavern simulation.

Create the circumstances for DAY {day_number}.

Generate:

- weather
- tavern event
- general mood
- special event

These should create opportunities for NPCs to behave differently.

Characters should NOT be directly controlled.

Only influence the circumstances.

Return ONLY JSON:

{{
    "weather": "...",
    "tavern_event": "...",
    "general_mood": "...",
    "special_event": "..."
}}
"""

    response = llm.invoke(
        prompt
    )

    try:

        data = json.loads(
            response.content
        )

    except Exception:

        data = {
            "weather": "Rainy",
            "tavern_event": "Few customers arrive.",
            "general_mood": "Quiet",
            "special_event": "A traveling merchant arrives."
        }

    return WorldState(
        day_number=day_number,
        weather=data["weather"],
        tavern_event=data["tavern_event"],
        general_mood=data["general_mood"],
        special_event=data["special_event"]
    )