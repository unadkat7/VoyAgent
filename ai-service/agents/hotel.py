from graph.state import TravelState
from tools.hotel_search import search_hotels


# ============================================================
# HOTEL NODE
# ============================================================

def hotel_node(state: TravelState):

    print("\n===================================")
    print("Hotel Agent")
    print("===================================\n")

    planner = state["planner_output"]

    hotel_output = search_hotels(planner)

    print("\nGenerated Hotels\n")

    for hotel in hotel_output.hotels:

        print(f"- {hotel.name}")

    return {
        "hotel_output": hotel_output,
    }