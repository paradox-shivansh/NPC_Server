from config import llm
from models.schemas import MemoryDecision


router_llm = llm.with_structured_output(
    MemoryDecision
)


def route_memory(user_message: str):

    prompt = f"""
You are a memory routing system for an intelligent chatbot.

Your job is to analyze the user's message and decide:

1. What is the user's intent?
2. Which memories should be retrieved?
3. Which memories should be written?
4. How important is this information?

AVAILABLE MEMORY TYPES:

ENTITY MEMORY:
Stores facts, preferences, attributes and relationships
about people and entities.

Examples:
- "My favorite language is Python"
- "My name is Jhon Snow"
- "I like Drinking Bear"
- "I live in a mideval town"
- "i have a tavorn called The Drunken Dragon"


EPISODIC MEMORY:
Stores important events and experiences.

Examples:
- "Yesterday I Met a very handsome man"
- "I failed to clear my clerk exam at castle"
- "I want had a nightmare about my wife leaving me"

SUMMARY MEMORY:
Stores conversation summaries and ongoing context.

REFLECTION MEMORY:
Stores lessons learned from previous interactions.

CHARACTER MEMORY:
Stores the chatbot's personality and behavioral traits.

IMPORTANT RULE:

Do NOT store every message.

Only store information that could be useful in future conversations.

User message:

{user_message}
"""

    decision = router_llm.invoke(prompt)

    return decision