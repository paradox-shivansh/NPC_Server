from pydantic import BaseModel
from typing import List

from config import llm


class EntityFact(BaseModel):

    entity: str

    fact: str

    importance: float


class EntityExtraction(BaseModel):

    facts: List[EntityFact]


entity_llm = llm.with_structured_output(
    EntityExtraction
)


def extract_entity_memory(user_message: str):

    prompt = f"""
Extract ONLY useful long-term facts from this message.

Useful facts include:

- Name
- Preferences
- Interests
- Skills
- Relationships
- Long-term goals
- Important personal facts

Do not extract temporary information unless it is
important for future conversations.

User message:

{user_message}
"""

    result = entity_llm.invoke(prompt)

    return result