import threading

from events.event_queue import PlayerEvent


class PlayerInput:

    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.running = True

    def start(self):
        thread = threading.Thread(
            target=self._listen,
            daemon=True
        )

        thread.start()

        return thread

    def _listen(self):

        print("\n🎒 Traveler input enabled.")
        print("Type something and press ENTER.")
        print("Type 'quit' to stop the simulation.\n")

        while self.running:

            try:
                message = input("\nTraveler > ")

            except EOFError:
                break

            except KeyboardInterrupt:
                break

            message = message.strip()

            if not message:
                continue

            if message.lower() == "quit":

                self.event_queue.put(
                    PlayerEvent(
                        event_type="quit",
                        message=""
                    )
                )

                self.running = False
                break

            self.event_queue.put(
                PlayerEvent(
                    event_type="speak",
                    message=message
                )
            )

    def stop(self):
        self.running = False