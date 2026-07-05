from graph.state import TravelState


# ============================================================
# SUPERVISOR NODE
# ============================================================

def supervisor_node(state: TravelState):

    print("\n========================================")
    print("Supervisor Agent")
    print("========================================")
    print("Starting travel planning workflow...\n")

    return {
        "current_agent": "planner"
    }
