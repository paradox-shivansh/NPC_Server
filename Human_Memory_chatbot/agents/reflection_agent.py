from config import llm
from models.schemas import ReflectionResult


reflection_llm = llm.with_structured_output(
    ReflectionResult
)


def reflect(
    user_message: str,
    assistant_response: str
):

    prompt = f"""
You are a self-reflection system for an intelligent chatbot.

Analyze the following interaction.

USER:

{user_message}

ASSISTANT:

{assistant_response}

Determine:

1. Did we learn anything useful about the user?
2. What should the assistant learn from this interaction?
3. Was there an important event?
4. Should the chatbot's behavior change?
5. If behavior should change, suggest SMALL controlled changes.

IMPORTANT:

Do not overreact to a single conversation.

Personality changes should only be suggested
when there is meaningful evidence.

Return structured output.
"""

    result = reflection_llm.invoke(prompt)

    return result