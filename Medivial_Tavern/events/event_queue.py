from queue import Queue
from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerEvent:
    event_type: str
    message: str
    target: Optional[str] = None


class PlayerEventQueue:

    def __init__(self):
        self.queue = Queue()

    def put(self, event: PlayerEvent):
        self.queue.put(event)

    def get(self):
        if self.queue.empty():
            return None

        return self.queue.get()

    def has_events(self):
        return not self.queue.empty()