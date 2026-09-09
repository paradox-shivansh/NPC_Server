from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)


class NPCState(TypedDict):

    npc: object
    world: object
    characters: list
    decision: dict


def build_npc_graph():

    def decision_node(state):

        npc = state["npc"]

        decision = npc.decide(
            world_state=state["world"].to_dict(),
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