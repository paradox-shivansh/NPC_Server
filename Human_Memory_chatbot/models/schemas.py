from pydantic import BaseModel, Field
from typing import List, Literal


class MemoryDecision(BaseModel):
    """
    Decides how the current user message
    should interact with the memory system.
    """

    intent: Literal[
        "casual_chat",
        "question",
        "personal_information",
        "preference",
        "event",
        "relationship",
        "correction",
        "personality_feedback",
        "emotional_context"
    ]

    retrieve_memories: List[
        Literal[
            "entity",
            "episodic",
            "summary",
            "reflection",
            "character"
        ]
    ]

    write_memories: List[
        Literal[
            "entity",
            "episodic",
            "summary",
            "reflection",
            "character",
            "none"
        ]
    ]

    importance: float = Field(
        ge=0.0,
        le=1.0
    )

    reasoning: str


class ReflectionResult(BaseModel):

    interaction_quality: float = Field(
        ge=0.0,
        le=1.0
    )

    learned_about_user: List[str]

    lessons_for_assistant: List[str]

    should_update_character: bool

    character_updates: List[str]

    important_episode: bool

    episode_summary: str