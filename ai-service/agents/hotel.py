from langchain_core.prompts import ChatPromptTemplate
from llm.gemini import llm
from schemas.hotel import HotelRecommendations
from graph.state import TravelState


# 1. Hotel Prompt

hotel_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Hotel Recommendation Agent of VoyAgent.

Your ONLY responsibility is recommending hotels.

You will receive TripRequirements.

Recommend exactly 3 hotels.

Recommendations should match:

- destination
- budget
- travel style

Do NOT generate flights.

Do NOT generate itinerary.

Return ONLY the HotelRecommendations schema.
"""
        ),

        (
            "human",
            "{trip_requirements}"
        ),
    ]
)


# 2. Hotel LLM

hotel_llm = llm.with_structured_output(
    HotelRecommendations
)


# 3. Hotel Chain
hotel_chain = hotel_prompt | hotel_llm


# 4. Hotel Node

def hotel_node(state: TravelState):

    print("\n===================================")
    print("Hotel Agent")
    print("===================================\n")

    planner = state["planner_output"]

    hotel_output = hotel_chain.invoke(
        {
            "trip_requirements":
            planner.model_dump_json(indent=2)
        }
    )

    print(hotel_output.model_dump_json(indent=2))

    return {

        "hotel_output": hotel_output

    }
