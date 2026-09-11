from memory.memory_system import NPCMemorySystem
from agents.decision_agent import DecisionAgent


class NPCAgent:

    def __init__(
        self,
        npc_id,
        name,
        role,
        personality,
        mood,
        llm
    ):

        self.npc_id = npc_id
        self.name = name
        self.role = role
        self.personality = personality
        self.mood = mood
        self.llm = llm

        # -----------------------------------------
        # MEMORY
        # -----------------------------------------

        self.memory = NPCMemorySystem(
            npc_id
        )

        # -----------------------------------------
        # DECISION AGENT
        # -----------------------------------------

        self.decision_agent = DecisionAgent(
            llm
        )

    # =============================================
    # DECISION
    # =============================================

    def decide(
    self,
    world_state,
    characters,
    active_conversation=None
        ):

        return self.decision_agent.decide(
        npc=self,
        world_state=world_state,
        available_npcs=characters,
        active_conversation=active_conversation
            )

    # =============================================
    # MOOD
    # =============================================

    def update_mood(
        self,
        new_mood
    ):

        self.mood = new_mood

    # =============================================
    # SPEAK
    # =============================================

    def speak(
        self,
        target,
        conversation,
        world_state
    ):

        memory_context = self.memory.retrieve(
            query=f"""
            Conversation with {target}

            Previous conversation:
            {conversation}
            """
        )

        prompt = f"""
You are {self.name}, a character living inside
a medieval tavern simulation.

ROLE:
{self.role}

PERSONALITY:
{self.personality}

CURRENT MOOD:
{self.mood}

WORLD STATE:
{world_state}

MEMORY:
{memory_context}

You are currently speaking to:
{target}

The conversation may contain multiple NPCs.

If several NPCs are present, you may address
one specific NPC or the entire group.

React naturally to what has actually been said.

PREVIOUS CONVERSATION:
{conversation}

RULES:

1. Stay completely in character.
2. Never mention that you are an AI.
3. Never describe your internal reasoning.
4. Only produce dialogue.
5. Do not narrate actions.
6. Remember previous interactions.
7. Let your mood affect your speech.
8. Let your personality affect your speech.
9. Do not repeat previous dialogue.
10. Relationships should evolve naturally.
11. React to what the other character actually said.
12. Do not suddenly know information that your character
    could not reasonably know.

Generate the next thing you would say.
"""

        response = self.llm.invoke(
            prompt
        )

        return response.content

    # =============================================
    # MEMORY
    # =============================================

    def remember_episode(
        self,
        episode,
        importance=0.5
    ):

        self.memory.remember_episode(
            episode,
            importance
        )

    # ---------------------------------------------

    def remember_entity(
        self,
        entity,
        fact,
        importance=0.5
    ):

        self.memory.remember_entity(
            entity,
            fact,
            importance
        )

    # ---------------------------------------------

    def remember_reflection(
        self,
        lesson,
        importance=0.5
    ):

        self.memory.remember_reflection(
            lesson,
            importance
        )

    # ---------------------------------------------

    def update_character(
        self,
        traits
    ):

        self.memory.update_character(
            traits
        )

    # ---------------------------------------------

    def get_character(
        self
    ):

        return self.memory.get_character()