from graph.state import TravelState


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: TravelState):

    planner = state["planner_output"]

    print("\n========================================")
    print("Router Agent")
    print("========================================")

    if planner.missing_fields:

        print("Missing information detected.")

        return {
            "current_agent": "clarification"
        }

    print("All required information collected.")

    return {
        "current_agent": "planning",
        "clarification_output": None
    }


# ============================================================
# ROUTING FUNCTION
# ============================================================

def route_after_router(state: TravelState):

    return state["current_agent"]