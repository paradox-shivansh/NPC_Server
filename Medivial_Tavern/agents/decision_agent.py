from typing import Literal

from pydantic import BaseModel, Field


# =========================================================
# ACTION DECISION
# =========================================================

class ActionDecision(BaseModel):

    action: Literal[
        "talk",
        "work",
        "wander",
        "rest",
        "join_conversation",
        "interrupt",
    ]

    target: str | None = None

    reason: str = ""

    initiative: int = Field(
        default=3,
        ge=1,
        le=5
    )

    message: str | None = None

    work_task: str | None = None


# =========================================================
# DECISION AGENT
# =========================================================

class DecisionAgent:

    def __init__(self, llm):

        self.llm = llm

        self.chain = llm.with_structured_output(
            ActionDecision
        )


    # =====================================================
    # DECIDE
    # =====================================================

    def decide(
        self,
        npc,
        world_state,
        available_npcs,
        active_conversation=None
    ):

        prompt = f"""

You are the autonomous decision-making system
for a medieval tavern NPC.

==================================================
NPC
==================================================

Name:
{npc.name}

Role:
{npc.role}

Personality:
{npc.personality}

Current mood:
{npc.mood}


==================================================
WORLD
==================================================

{world_state}


==================================================
OTHER NPCS
==================================================

{available_npcs}


==================================================
ACTIVE CONVERSATION
==================================================

{active_conversation}


==================================================
YOUR TASK
==================================================

Decide what this NPC wants to do right now.

The NPC should behave as an autonomous character.

Personality, mood, role, relationships, world events,
work responsibilities and current conversations should
influence the decision.


==================================================
AVAILABLE ACTIONS
==================================================

1. talk

Start a new conversation with another NPC.

Use this when the NPC wants to socialize,
ask something, share information, flirt,
complain, discuss an event, etc.


2. work

Perform normal responsibilities.

Examples:

- clean tables
- serve customers
- prepare food
- manage the tavern
- organize supplies


3. wander

Move around the tavern or inspect the environment.


4. rest

Take a break when the NPC has a believable reason
to rest.


5. join_conversation

Join an existing conversation because the NPC has
something relevant to contribute.

This is NOT necessarily an interruption.

Example:

John and Eva are discussing the traveling bards.

Freddy hears them and wants to tell them that the
bards have not paid for their rooms.

Freddy can join the conversation.


6. interrupt

Interrupt an existing conversation because the NPC
has a sufficiently important or believable reason.

An interruption should NOT happen constantly.

Only interrupt when there is a meaningful reason.


==================================================
INTERRUPTION BEHAVIOR
==================================================

NPCs are autonomous.

They can observe what other NPCs are doing.

They do NOT have to wait for conversations to finish.

They may interrupt when appropriate.


For Freddy:

Freddy is the tavern owner.

He cares about:

- keeping the tavern running
- customers
- cleanliness
- money
- work getting completed

Freddy may interrupt Eva if:

- Eva is talking instead of working
- tables need cleaning
- customers need attention
- food needs preparing
- the tavern is becoming messy
- something important requires Eva
- Freddy is frustrated by the situation


Example:

John and Eva are talking.

The tavern has several dirty tables.

Freddy may decide:

action:
interrupt

target:
Eva

message:
"Eva, enough chatting. Table three needs cleaning."

work_task:
"clean table three"


==================================================
OTHER NPCS
==================================================

Eva may interrupt when:

- she needs help
- a customer needs attention
- she has important information
- something interesting happens


John may interrupt when:

- he has something relevant to say
- he wants to join the conversation
- something catches his attention
- he wants to defend someone
- he wants to continue a discussion


==================================================
IMPORTANT RULES
==================================================

1. Do not make every NPC talk constantly.

2. Do not make every NPC interrupt constantly.

3. NPCs should sometimes work, wander or rest.

4. Personality should strongly influence decisions.

5. Mood should influence decisions.

6. Freddy should behave like a tavern owner.

7. Eva should naturally be more social.

8. John should naturally enjoy social interaction.

9. An interruption must have a believable reason.

10. If action is "interrupt", target must be
the NPC being addressed.

11. If action is "interrupt", message should be
the actual dialogue spoken aloud.

12. If the interruption gives somebody a work order,
provide work_task.

13. If action is "join_conversation", target may be
the conversation participant the NPC is addressing.

14. Do not invent information that is not available
in the world or conversation.

15. Do not repeatedly select the same action without
a reason.

16. Consider the active conversation when deciding
whether to interrupt or join.


==================================================
INTERRUPTION EXAMPLE
==================================================

Active conversation:

John:
"I was telling Eva about the traveling bards."

Eva:
"They seem quite talented."

World:
"Three tables are dirty."

Freddy personality:
"Responsible tavern owner who is frustrated
about the tavern losing money."

Good decision:

action:
interrupt

target:
Eva

reason:
"Eva should be helping maintain the tavern because
there is work waiting."

message:
"Eva, stop chatting for a moment. Table three needs cleaning."

work_task:
"clean table three"


==================================================
JOIN CONVERSATION EXAMPLE
==================================================

Active conversation:

John:
"Did you hear the bards' ballad?"

Eva:
"No, I only heard part of it."

Freddy:
"I heard the entire thing."

Good decision:

action:
join_conversation

target:
John

message:
"I heard the entire ballad. You should have seen
the crowd when they mentioned hidden fortunes."


==================================================
OUTPUT
==================================================

Return ONLY the structured ActionDecision.

"""


        # =================================================
        # CALL LLM
        # =================================================

        try:

            result = self.chain.invoke(
                prompt
            )

            # ---------------------------------------------
            # SAFETY CLAMP
            # ---------------------------------------------

            result.initiative = max(
                1,
                min(
                    5,
                    result.initiative
                )
            )

            return result


        # =================================================
        # FALLBACK
        # =================================================

        except Exception as e:

            print(
                f"⚠️ Decision error for "
                f"{npc.name}: {e}"
            )

            targets = [
                name
                for name in available_npcs
                if name != npc.name
            ]

            return ActionDecision(

                action="talk",

                target=(
                    targets[0]
                    if targets
                    else None
                ),

                initiative=3,

                reason="Fallback decision"

            )