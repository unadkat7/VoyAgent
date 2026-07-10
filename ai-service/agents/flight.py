from graph.state import TravelState
from tools.flight_search import search_flights


# ============================================================
# FLIGHT NODE
# ============================================================

def flight_node(state: TravelState):

    print("\n===================================")
    print("Flight Agent")
    print("===================================\n")

    planner = state["planner_output"]

    flight_output = search_flights(planner)

    print("\nGenerated Flights\n")

    for flight in flight_output.flights:

        print(f"- {flight.airline} ({flight.flight_number}) | {flight.departure_airport} -> {flight.arrival_airport} | {flight.currency} {flight.price}")

    return {

        "flight_output": flight_output,

        "current_agent": "flight"

    }
