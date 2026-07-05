from langchain_core.prompts import ChatPromptTemplate
from llm.gemini import llm
from schemas.flight import FlightRecommendations
from graph.state import TravelState


# 1.1 Flight Prompt
flight_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Flight Recommendation Agent of VoyAgent.

Your ONLY responsibility is recommending flights.

You will receive TripRequirements.

Recommend exactly 3 suitable flight options.

Recommendations should consider:

- destination
- budget
- travel style
- travelers

Return ONLY the FlightRecommendations schema.

Do NOT generate:

- hotels
- itinerary
- travel tips
"""
        ),

        (
            "human",
            "{planner_output}"
        ),
    ]
)


# 2.1 Flight LLM
flight_llm = llm.with_structured_output(
    FlightRecommendations
)


# 3.1 Flight Chain
flight_chain = flight_prompt | flight_llm


# 4.1 Flight Node
def flight_node(state: TravelState):

    print("\n===================================")
    print("Flight Agent")
    print("===================================\n")

    planner = state["planner_output"]

    flight_output = flight_chain.invoke(
        {
            "planner_output":
            planner.model_dump_json(indent=2)
        }
    )

    print("\nGenerated Flights\n")

    for flight in flight_output.flights:

        print(f"- {flight.airline}")

    return {

        "flight_output": flight_output,

        "current_agent":"flight"

    }
