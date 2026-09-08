from agents.decision_agent import decide_action

from memory.memory_system import NPCMemorySystem


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


        self.memory = NPCMemorySystem(

            npc_id

        )


    def decide(

        self,

        world_state,

        characters

    ):


        return decide_action(

            llm=self.llm,

            npc_name=self.name,

            personality=self.personality,

            mood=self.mood,

            world_state=world_state,

            available_characters=characters

        )


    def speak(

        self,

        target,

        conversation,

        world_state

    ):


        memories = self.memory.retrieve(

            conversation

        )


        prompt = f"""
You are {self.name}.

ROLE:

{self.role}

PERSONALITY:

{self.personality}

CURRENT MOOD:

{self.mood}

WORLD STATE:

{world_state}

RELEVANT MEMORIES:

{memories}

CONVERSATION:

{conversation}

Respond naturally.

Stay in character.

Do not narrate actions.

Only generate dialogue.
"""


        response = self.llm.invoke(

            prompt

        )


        return response.content


    def remember_episode(

        self,

        episode,

        importance=0.5

    ):

        self.memory.episodic.add_episode(

            content=episode,

            importance=importance

        )