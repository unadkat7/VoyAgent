from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from schemas.planner import TripRequirements, ClarificationResponse
from schemas.hotel import HotelRecommendations
from schemas.flight import FlightRecommendations
from schemas.itinerary import DetailedItinerary
from schemas.final import FinalTravelPlan


# ============================================================
# STATE
# ============================================================

class TravelState(TypedDict):

    # Complete conversation
    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    # Current active agent
    current_agent: str | None

    # Planner output
    planner_output: TripRequirements | None

    clarification_output: ClarificationResponse | None

    # Future agents
    hotel_output: HotelRecommendations | None

    flight_output: FlightRecommendations | None

    itinerary_output: DetailedItinerary | None

    final_output: FinalTravelPlan | None
