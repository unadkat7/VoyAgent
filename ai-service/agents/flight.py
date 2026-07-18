from graph.state import TravelState
from tools.flight_search import search_flights


# ============================================================
# FLIGHT NODE
# ============================================================

def flight_node(state: TravelState):
    planner = state["planner_output"]
    flight_output = search_flights(planner)

    return {
        "flight_output": flight_output,
    }
