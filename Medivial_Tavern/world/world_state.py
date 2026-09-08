class WorldState:


    def __init__(

        self,

        day_number,

        weather,

        tavern_condition,

        event

    ):


        self.day_number = day_number

        self.weather = weather

        self.tavern_condition = tavern_condition

        self.event = event


    def to_dict(self):

        return {

            "day": self.day_number,

            "weather": self.weather,

            "tavern_condition": self.tavern_condition,

            "event": self.event

        }