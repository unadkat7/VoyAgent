from graph.state import TravelState
from tools.hotel_search import search_hotels


# ============================================================
# HOTEL NODE
# ============================================================

def hotel_node(state: TravelState):
    planner = state["planner_output"]
    hotel_output = search_hotels(planner)

    return {
        "hotel_output": hotel_output,
    }