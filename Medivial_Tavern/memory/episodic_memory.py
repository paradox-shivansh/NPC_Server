import uuid

import chromadb


class EpisodicMemory:

    def __init__(self, npc_id):

        self.npc_id = npc_id


        self.client = chromadb.PersistentClient(

            path=f"data/{npc_id}/chroma"

        )


        self.collection = self.client.get_or_create_collection(

            name="episodes"

        )


    def add_episode(

        self,

        content,

        importance=0.5

    ):

        episode_id = str(uuid.uuid4())


        self.collection.add(

            ids=[episode_id],

            documents=[content],

            metadatas=[

                {

                    "importance": importance

                }

            ]

        )


    def retrieve(

        self,

        query,

        limit=5

    ):

        if self.collection.count() == 0:

            return []


        results = self.collection.query(

            query_texts=[query],

            n_results=min(

                limit,

                self.collection.count()

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

            in zip(documents, metadatas)

        ]