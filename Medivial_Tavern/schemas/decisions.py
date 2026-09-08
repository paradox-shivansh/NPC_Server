from typing import Literal

from pydantic import BaseModel


class NPCDecision(

    BaseModel

):

    action: Literal[

        "talk",

        "wait",

        "interrupt",

        "leave"

    ]


    target: str | None = None


    reason: str


    urgency: float