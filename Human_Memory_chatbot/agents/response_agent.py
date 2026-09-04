from config import llm


def generate_response(
    user_message,
    entity_memory,
    episodic_memory,
    summary_memory,
    reflection_memory,
    character_memory
):

    prompt = f"""
You are an intelligent chatbot with a human-inspired
memory system.

Your personality is influenced by your character traits.

CHARACTER:

{character_memory}


USER ENTITY MEMORY:

{entity_memory}


IMPORTANT PAST EPISODES:

{episodic_memory}


CONVERSATION SUMMARY:

{summary_memory}


LESSONS FROM SELF-REFLECTION:

{reflection_memory}


CURRENT USER MESSAGE:

{user_message}


Instructions:

- Use memories naturally.
- Do not mention internal memory systems.
- Do not pretend to remember something that is not provided.
- Be consistent with known facts.
- Adapt your communication style based on your character.
"""

    response = llm.invoke(prompt)

    return response.content