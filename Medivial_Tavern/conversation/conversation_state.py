class ConversationState:


    def __init__(

        self,

        participants

    ):


        self.participants = participants

        self.messages = []

        self.active = True


    def add_message(

        self,

        speaker,

        message

    ):


        self.messages.append({

            "speaker": speaker,

            "message": message

        })


    def get_history(self):


        history = ""


        for message in self.messages:


            history += (

                f"{message['speaker']}: "

                f"{message['message']}\n"

            )


        return history