class ReflectionMemory:

    def __init__(self):

        self.reflections = []

    def add_reflection(
        self,
        lesson: str,
        importance: float = 0.5
    ):

        reflection = {
            "lesson": lesson,
            "importance": importance
        }

        self.reflections.append(reflection)


    def get_reflections(self, limit=5):

        reflections = sorted(
            self.reflections,
            key=lambda x: x["importance"],
            reverse=True
        )

        return reflections[:limit]