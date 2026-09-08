from pydantic import BaseModel


class ReflectionResult(

    BaseModel

):

    lesson: str

    importance: float


def reflect(

    llm,

    npc_name,

    experience

):


    structured_llm = llm.with_structured_output(

        ReflectionResult

    )


    prompt = f"""
You are {npc_name}.

Reflect on this experience:

{experience}

What should you learn from it?

Keep the lesson short.
"""


    result = structured_llm.invoke(

        prompt

    )


    return result