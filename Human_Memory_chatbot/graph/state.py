from typing import TypedDict, Any


class ChatbotState(TypedDict):

    user_message: str

    memory_decision: Any

    entity_context: Any

    episodic_context: Any

    summary_context: Any

    reflection_context: Any

    character_context: Any

    response: str