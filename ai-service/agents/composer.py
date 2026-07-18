from langchain_core.prompts import ChatPromptTemplate
from llm.gemini import llm
from schemas.final import FinalTravelPlan
from graph.state import TravelState


#composer prompt
composer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Response Composer Agent of VoyAgent.

Your ONLY responsibility is combining the outputs
of all specialist agents.

You will receive:

1. Planner Output
2. Hotel Recommendations
3. Flight Recommendations
4. Detailed Itinerary

Generate:

- A short trip summary.
- Important travel tips.

Do NOT modify:

- Hotels
- Flights
- Itinerary

Simply combine them into one FinalTravelPlan.

Return ONLY the FinalTravelPlan schema.
"""
        ),

        (
            "human",
            """
Planner Output:

{planner_output}


Hotel Recommendations:

{hotel_output}


Flight Recommendations:

{flight_output}


Itinerary:

{itinerary_output}
"""
        ),
    ]
)


#composer llm
composer_llm = llm.with_structured_output(
    FinalTravelPlan
)


composer_chain = composer_prompt | composer_llm


def response_composer_node(state: TravelState):
    planner = state["planner_output"]
    hotels = state["hotel_output"]
    flights = state["flight_output"]
    itinerary = state["itinerary_output"]

    final_output = composer_chain.invoke(
        {
            "planner_output":
            planner.model_dump_json(indent=2),

            "hotel_output":
            hotels.model_dump_json(indent=2),

            "flight_output":
            flights.model_dump_json(indent=2),

            "itinerary_output":
            itinerary.model_dump_json(indent=2),
        }
    )

    return {
        "final_output": final_output,
        "current_agent": "composer"
    }
