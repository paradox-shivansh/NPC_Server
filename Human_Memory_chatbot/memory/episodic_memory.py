from datetime import datetime


class EpisodicMemory:

    def __init__(self):

        self.episodes = []

    def add_episode(
        self,
        content: str,
        importance: float
    ):

        episode = {
            "content": content,
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        }

        self.episodes.append(episode)

    def get_relevant_episodes(
        self,
        limit: int = 5
    ):

        episodes = sorted(
            self.episodes,
            key=lambda x: x["importance"],
            reverse=True
        )

        return episodes[:limit]

    def get_all(self):

        return self.episodes