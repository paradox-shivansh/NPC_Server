from memory.entity_memory import EntityMemory

from memory.episodic_memory import EpisodicMemory

from memory.summary_memory import SummaryMemory

from memory.reflection_memory import ReflectionMemory

from memory.character_memory import CharacterMemory

from memory.relationship_memory import RelationshipMemory

from memory.memory_router import MemoryRouter


class NPCMemorySystem:


    def __init__(

        self,

        npc_id

    ):

        self.npc_id = npc_id


        self.entity = EntityMemory(

            npc_id

        )


        self.episodic = EpisodicMemory(

            npc_id

        )


        self.summary = SummaryMemory(

            npc_id

        )


        self.reflection = ReflectionMemory(

            npc_id

        )


        self.character = CharacterMemory(

            npc_id

        )


        self.relationship = RelationshipMemory(

            npc_id

        )


        self.router = MemoryRouter()


    def retrieve(

        self,

        query

    ):

        memory_types = self.router.route(

            query

        )


        result = {}


        if "episodic" in memory_types:

            result["episodes"] = (

                self.episodic.retrieve(

                    query

                )

            )


        if "entity" in memory_types:

            result["entities"] = (

                self.entity.search_memory(

                    query

                )

            )


        result["summary"] = (

            self.summary.get_latest()

        )


        result["reflections"] = (

            self.reflection.get_reflections()

        )


        result["character"] = (

            self.character.get_traits()

        )


        return result