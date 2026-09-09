import json


class ReviewerAgent:

    def __init__(self, llm):

        self.llm = llm


    def review(
        self,
        conversation
    ):

        prompt = f"""
You are a conversation reviewer for a medieval tavern simulation.

Analyze this conversation:

{conversation}

Determine whether the conversation should continue.

Return ONLY valid JSON:

{{
    "should_end": true_or_false,
    "reason": "short reason",
    "new_topic": "possible new topic"
}}

The conversation should end if:

- it becomes repetitive
- neither character has anything meaningful to say
- the characters naturally reach a stopping point

The conversation should continue if:

- there is unresolved tension
- a relationship is developing
- a new topic can naturally emerge
- something important is happening
"""

        response = self.llm.invoke(
            prompt
        )

        try:

            return json.loads(
                response.content
            )

        except Exception:

            return {
                "should_end": False,
                "reason": "Reviewer parsing failed",
                "new_topic": ""
            }