from pydantic import BaseModel


class ConversationReview(

    BaseModel

):

    quality: float

    repetitive: bool

    should_end: bool

    recommendation: str


class ReviewerAgent:


    def __init__(

        self,

        llm

    ):

        self.llm = llm.with_structured_output(

            ConversationReview

        )


    def review(

        self,

        conversation

    ):


        prompt = f"""
You are reviewing an NPC conversation.

Check:

Is the conversation repetitive?

Is it progressing naturally?

Should the conversation end?

Conversation:

{conversation}

Return your evaluation.
"""


        result = self.llm.invoke(

            prompt

        )


        return result.model_dump()