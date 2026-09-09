from typing import Literal
from pydantic import BaseModel, Field


class ActionDecision(BaseModel):
    action: Literal[
        "talk",
        "work",
        "wander",
        "rest"
    ]

    target: str | None = None

    initiative: int = Field(
        default=3
    )

    reason: str = ""


class DecisionAgent:

    def __init__(self, llm):
        self.llm = llm

        self.chain = llm.with_structured_output(
            ActionDecision
        )

    def decide(
        self,
        npc,
        world_state,
        available_npcs
    ):

        prompt = f"""
You are the decision-making system for an autonomous medieval tavern NPC.

NPC:
Name: {npc.name}
Role: {npc.role}
Personality: {npc.personality}
Current mood: {npc.mood}

World:
{world_state}

Other NPCs:
{available_npcs}

Decide what this NPC wants to do right now.

Possible actions:

1. talk
   - Start or join a conversation.
   - If talking, choose another NPC as target.

2. work
   - Perform their normal tavern-related responsibilities.

3. wander
   - Move around, observe the tavern, inspect something, etc.

4. rest
   - Sit down, eat, drink, relax, etc.

IMPORTANT:

- NPCs should behave autonomously.
- Do not make everyone talk every turn.
- Personality and mood should influence decisions.
- Eva is naturally social.
- Freddy may focus on the tavern's financial situation.
- John enjoys socializing and especially likes talking to Eva.
- The same NPC should not repeatedly choose the same action without reason.
- If action is "talk", target must be another NPC.
- initiative should be between 1 and 5.

Return only the structured decision.
"""

        try:
            result = self.chain.invoke(prompt)

            # Keep initiative safe even if the model gives
            # an unexpected value.
            result.initiative = max(
                1,
                min(5, result.initiative)
            )

            return result

        except Exception as e:

            print(
                f"⚠️ Decision error for {npc.name}: {e}"
            )

            # Safe fallback
            targets = [
                name
                for name in available_npcs
                if name != npc.name
            ]

            return ActionDecision(
                action="talk",
                target=targets[0] if targets else None,
                initiative=3,
                reason="Fallback decision"
            )