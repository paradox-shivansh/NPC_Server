from memory.episodic_memory import EpisodicMemory
from memory.entity_memory import EntityMemory
from memory.reflection_memory import ReflectionMemory
from memory.summary_memory import SummaryMemory
from memory.character_memory import CharacterMemory


class NPCMemorySystem:

    def __init__(self, npc_id: str):

        self.npc_id = npc_id

        # =============================================
        # INDIVIDUAL MEMORY SYSTEMS
        # =============================================

        self.episodic = EpisodicMemory(npc_id)
        self.entity = EntityMemory(npc_id)
        self.reflection = ReflectionMemory(npc_id)
        self.summary = SummaryMemory(npc_id)
        self.character = CharacterMemory(npc_id)

    # =============================================
    # WRITE MEMORY
    # =============================================

    def remember_episode(
        self,
        content,
        importance=0.5
    ):

        return self.episodic.add_episode(
            content=content,
            importance=importance
        )

    # ---------------------------------------------

    def remember_entity(
        self,
        entity,
        fact,
        importance=0.5
    ):

        return self.entity.add_memory(
            entity=entity,
            fact=fact,
            importance=importance
        )

    # ---------------------------------------------

    def remember_reflection(
        self,
        lesson,
        importance=0.5
    ):

        return self.reflection.add_reflection(
            lesson=lesson,
            importance=importance
        )

    # ---------------------------------------------

    def update_character(
        self,
        traits
    ):

        return self.character.update_traits(
            traits
        )

    # =============================================
    # READ MEMORY
    # =============================================

    def retrieve(
        self,
        query
    ):

        episodic = self.episodic.retrieve(
            query=query,
            limit=5
        )

        entities = self.entity.retrieve(
            limit=5
        )

        reflections = self.reflection.get_reflections(
            limit=3
        )

        summary = self.summary.get_latest()

        character = self.character.get_traits()

        return {
            "episodic": episodic,
            "entities": entities,
            "reflections": reflections,
            "summary": summary,
            "character": character
        }

    # =============================================
    # INDIVIDUAL MEMORY ACCESS
    # =============================================

    def get_character(self):

        return self.character.get_traits()

    # ---------------------------------------------

    def get_entities(self):

        return self.entity.retrieve(
            limit=10
        )

    # ---------------------------------------------

    def get_reflections(self):

        return self.reflection.get_reflections(
            limit=10
        )

    # ---------------------------------------------

    def get_summary(self):

        return self.summary.get_latest()