from langgraph.graph import StateGraph, END,START

from typing import TypedDict


class NPCState(

    TypedDict

):

    world_state: dict

    characters: list

    decision: object


def build_npc_graph(

    npc

):


    def decision_node(

        state

    ):


        decision = npc.decide(

            world_state=state["world_state"],

            characters=state["characters"]

        )


        return {

            "decision": decision

        }


    workflow = StateGraph(

        NPCState

    )


    workflow.add_node(

        "decision",

        decision_node

    )


    workflow.set_entry_point(

        "decision"

    )


    workflow.add_edge(

        "decision",

        END

    )


    return workflow.compile()