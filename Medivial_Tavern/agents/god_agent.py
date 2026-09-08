from pydantic import BaseModel

from langchain_core.prompts import ChatPromptTemplate


class DayEvent(

    BaseModel

):

    description: str


class DailyWorld(

    BaseModel

):

    weather: str

    tavern_condition: str

    event: str

    eva_mood_change: float

    freddy_mood_change: float

    john_mood_change: float


def create_day(

    llm,

    day_number

):


    structured_llm = llm.with_structured_output(

        DailyWorld

    )


    prompt = ChatPromptTemplate.from_template(

        """
You are the God Entity controlling a medieval tavern simulation.

Create Day {day_number}.

Generate:

Weather.

Tavern condition.

One interesting event.

Small mood changes for:

Eva
Freddy
John

Keep events believable and suitable for a medieval tavern.

Do not directly control what characters say.
"""
    )


    chain = prompt | structured_llm


    return chain.invoke({

        "day_number": day_number

    })