class MemoryRouter:


    def route(

        self,

        query

    ):

        query = query.lower()


        retrieve = [

            "summary",

            "character"

        ]


        if any(

            word in query

            for word in [

                "remember",

                "before",

                "happened",

                "last time",

                "previous"

            ]

        ):

            retrieve.append(

                "episodic"

            )


        if any(

            word in query

            for word in [

                "eva",

                "freddy",

                "john"

            ]

        ):

            retrieve.append(

                "entity"

            )


        return retrieve