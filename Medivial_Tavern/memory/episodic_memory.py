import uuid

import chromadb

from pathlib import Path


class EpisodicMemory:

    def __init__(self, npc_id: str):

        self.npc_id = npc_id

        base_path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / npc_id
            / "chroma"
        )

        base_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=str(base_path)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="episodes"
            )
        )


    def add_episode(
        self,
        content,
        importance=0.5
    ):

        episode_id = str(
            uuid.uuid4()
        )

        self.collection.add(
            ids=[episode_id],

            documents=[content],

            metadatas=[
                {
                    "importance": float(
                        importance
                    )
                }
            ]
        )


    def retrieve(
        self,
        query,
        limit=5
    ):

        count = self.collection.count()

        if count == 0:
            return []

        results = self.collection.query(
            query_texts=[query],

            n_results=min(
                limit,
                count
            )
        )

        documents = results["documents"][0]

        metadatas = results["metadatas"][0]

        return [
            {
                "content": document,
                "metadata": metadata
            }

            for document, metadata
            in zip(
                documents,
                metadatas
            )
        ]