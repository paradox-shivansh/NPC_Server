from memory.entity_memory import EntityMemory
from memory.episodic_memory import EpisodicMemory
from memory.summary_memory import SummaryMemory
from memory.reflection_memory import ReflectionMemory
from memory.charecter_memory import CharacterMemory

from graph.chatbot_graph import build_graph
from database.database import initialize_database

# -----------------------
# INITIALIZE DATABASE
# -----------------------

initialize_database()


# -----------------------
# INITIALIZE MEMORIES
# -----------------------

entity_memory = EntityMemory()

episodic_memory = EpisodicMemory()

summary_memory = SummaryMemory()

reflection_memory = ReflectionMemory()

character_memory = CharacterMemory()


# -----------------------
# BUILD GRAPH
# -----------------------

chatbot = build_graph(
    entity_memory=entity_memory,
    episodic_memory=episodic_memory,
    summary_memory=summary_memory,
    reflection_memory=reflection_memory,
    character_memory=character_memory
)


# -----------------------
# CHAT LOOP
# -----------------------

print("🧠 Human Memory Chatbot Started")
print("Type 'exit' to stop.\n")


while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":

        print("Goodbye 👋")

        break


    result = chatbot.invoke({
        "user_message": user_message
    })


    print("\nBot:", result["response"])
    print()