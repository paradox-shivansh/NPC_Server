from collections import defaultdict


class EntityMemory:

    def __init__(self):

        self.entities = defaultdict(list)

    def add_memory(
        self,
        entity: str,
        fact: str,
        importance: float = 0.65
    ):

        memory = {
            "fact": fact,
            "importance": importance
        }

        # Prevent exact duplicates
        if memory not in self.entities[entity]:
            self.entities[entity].append(memory)

    def get_memories(self, entity: str):

        memories = self.entities.get(entity, [])

        sorted_memories = sorted(
            memories,
            key=lambda x: x["importance"],
            reverse=True
        )

        return sorted_memories

    def get_all(self):

        return dict(self.entities)