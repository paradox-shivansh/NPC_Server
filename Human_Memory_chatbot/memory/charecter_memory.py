class CharacterMemory:

    def __init__(self):

        self.traits = {

            "humor": 0.5,
            "empathy": 0.7,
            "curiosity": 0.8,
            "formality": 0.5,
            "confidence": 0.7
        }


    def get_traits(self):

        return self.traits


    def update_trait(
        self,
        trait: str,
        proposed_change: float
    ):

        if trait not in self.traits:
            return

        MAX_CHANGE = 0.05

        change = max(
            -MAX_CHANGE,
            min(proposed_change, MAX_CHANGE)
        )

        self.traits[trait] += change

        self.traits[trait] = max(
            0.0,
            min(1.0, self.traits[trait])
        )