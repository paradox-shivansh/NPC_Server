from langgraph.graph import StateGraph, END

from graph.state import ChatbotState

from memory.router import route_memory
from memory.entity_extractor import extract_entity_memory

from agents.response_agent import generate_response
from agents.reflection_agent import reflect


def build_graph(
    entity_memory,
    episodic_memory,
    summary_memory,
    reflection_memory,
    character_memory
):

    # -------------------------
    # MEMORY ROUTER
    # -------------------------

    def router_node(state):

        print("🧠 ROUTER NODE RUNNING")

        decision = route_memory(
            state["user_message"]
        )

        return {
            "memory_decision": decision
        }


    # -------------------------
    # RETRIEVE MEMORY
    # -------------------------

    def retrieve_memory_node(state):

        print("🔍 RETRIEVE MEMORY NODE RUNNING")

        decision = state["memory_decision"]

        entity_context = []
        episodic_context = []
        reflection_context = []

        # Character is always loaded
        character_context = character_memory.get_traits()

        if "entity" in decision.retrieve_memories:
            entity_context = entity_memory.get_all()

        if "episodic" in decision.retrieve_memories:
            episodic_context = episodic_memory.get_relevant_episodes()

        if "reflection" in decision.retrieve_memories:
            reflection_context = reflection_memory.get_reflections()

        summary_context = summary_memory.get_context()

        return {
            "entity_context": entity_context,
            "episodic_context": episodic_context,
            "reflection_context": reflection_context,
            "character_context": character_context,
            "summary_context": summary_context
        }


    # -------------------------
    # RESPONSE
    # -------------------------

    def response_node(state):

        print("🤖 RESPONSE NODE RUNNING")

        response = generate_response(
            user_message=state["user_message"],
            entity_memory=state["entity_context"],
            episodic_memory=state["episodic_context"],
            summary_memory=state["summary_context"],
            reflection_memory=state["reflection_context"],
            character_memory=state["character_context"]
        )

        return {
            "response": response
        }


    # -------------------------
    # REFLECTION
    # -------------------------

    def reflection_node(state):

        print("🤔 REFLECTION NODE RUNNING")

        try:

            result = reflect(
                user_message=state["user_message"],
                assistant_response=state["response"]
            )

            return {
                "reflection_result": result
            }

        except Exception as e:

            print(f"⚠️ Reflection failed: {e}")

            return {
                "reflection_result": None
            }


    # -------------------------
    # MEMORY UPDATE
    # -------------------------

    def memory_update_node(state):

        print("💾 MEMORY UPDATE NODE IS RUNNING")

        decision = state["memory_decision"]
        user_message = state["user_message"]

        # ENTITY MEMORY
        if "entity" in decision.write_memories:

            print("👤 Updating Entity Memory")

            extraction = extract_entity_memory(user_message)

            for item in extraction.facts:

                entity_memory.add_memory(
                    entity=item.entity,
                    fact=item.fact,
                    importance=item.importance
                )

        # EPISODIC MEMORY
        if "episodic" in decision.write_memories:

            print("📖 Updating Episodic Memory")

            episodic_memory.add_episode(
                content=user_message,
                importance=decision.importance
            )

        # REFLECTION MEMORY
        reflection_result = state.get("reflection_result")

        if reflection_result:

            print("🤔 Updating Reflection Memory")

            for lesson in reflection_result.lessons_for_assistant:

                reflection_memory.add_reflection(
                    lesson=lesson,
                    importance=reflection_result.interaction_quality
                )

        # SUMMARY MEMORY
        summary_memory.add_message(
            "user",
            user_message
        )

        summary_memory.add_message(
            "assistant",
            state["response"]
        )

        if summary_memory.should_summarize():
            summary_memory.update_summary()

        return {}


    # -------------------------
    # BUILD GRAPH
    # -------------------------

    workflow = StateGraph(ChatbotState)

    workflow.add_node("router", router_node)

    workflow.add_node(
        "retrieve_memory",
        retrieve_memory_node
    )

    workflow.add_node("response", response_node)

    workflow.add_node("reflection", reflection_node)

    workflow.add_node(
        "memory_update",
        memory_update_node
    )


    # -------------------------
    # EDGES
    # -------------------------

    workflow.set_entry_point("router")

    workflow.add_edge(
        "router",
        "retrieve_memory"
    )

    workflow.add_edge(
        "retrieve_memory",
        "response"
    )

    workflow.add_edge(
        "response",
        "reflection"
    )

    workflow.add_edge(
        "reflection",
        "memory_update"
    )

    workflow.add_edge(
        "memory_update",
        END
    )


    # -------------------------
    # COMPILE GRAPH
    # -------------------------

    app = workflow.compile()

    print("✅ GRAPH BUILT SUCCESSFULLY")
    print("Graph object:", app)

    return app