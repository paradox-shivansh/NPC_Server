from langgraph.graph import StateGraph, END

from typing import TypedDict


class SimulationState(

    TypedDict

):

    day_number: int

    world: object


def build_simulation_graph(

    create_day_function,

    run_simulation_function

):


    def day_node(

        state

    ):


        world = create_day_function(

            state["day_number"]

        )


        return {

            "world": world

        }


    def simulation_node(

        state

    ):


        run_simulation_function(

            state["world"]

        )


        return {}


    workflow = StateGraph(

        SimulationState

    )


    workflow.add_node(

        "create_day",

        day_node

    )


    workflow.add_node(

        "run_simulation",

        simulation_node

    )


    workflow.set_entry_point(

        "create_day"

    )


    workflow.add_edge(

        "create_day",

        "run_simulation"

    )


    workflow.add_edge(

        "run_simulation",

        END

    )


    return workflow.compile()