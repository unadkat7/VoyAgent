from api.planner import run_graph
from utils.display import (
    display_trip_requirements,
    display_clarification,
    display_hotel_recommendations,
    display_flight_recommendations,
    display_itinerary,
    display_final_travel_plan,
)


# ============================================================
# MAIN
# ============================================================



if __name__ == "__main__":

    print("\n========================================")
    print("        Welcome to VoyAgent")
    print("========================================\n")

    thread_id = "user-1"

    while True:

        user_input = input("You : ")

        if user_input.lower() == "exit":
            break

        result = run_graph(
            user_input,
            thread_id,
        )

        planner = result["planner_output"]

        display_trip_requirements(planner)

        if result["current_agent"] == "clarification":

            display_clarification(result["messages"][-1].content)

        else:

            display_hotel_recommendations(result["hotel_output"].hotels)

            if result.get("flight_output"):

                display_flight_recommendations(result["flight_output"].flights)

            if result.get("itinerary_output"):

                display_itinerary(result["itinerary_output"].itinerary)

            if result.get("final_output"):

                display_final_travel_plan(result["final_output"])