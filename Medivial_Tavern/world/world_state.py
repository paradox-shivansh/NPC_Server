class WorldState:

    def __init__(
        self,
        day_number,
        weather,
        tavern_event,
        general_mood,
        special_event
    ):

        self.day_number = day_number
        self.weather = weather
        self.tavern_event = tavern_event
        self.general_mood = general_mood
        self.special_event = special_event


    def to_dict(self):

        return {
            "day": self.day_number,
            "weather": self.weather,
            "tavern_event": self.tavern_event,
            "general_mood": self.general_mood,
            "special_event": self.special_event
        }


    def __str__(self):

        return str(
            self.to_dict()
        )