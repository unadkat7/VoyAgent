# ============================================================
# IMPORTS
# ============================================================

from dotenv import load_dotenv

from typing import TypedDict, Annotated

from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
)

from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import MemorySaver


load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)


# ============================================================
# PLANNER PROMPT
# ============================================================

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Planner Agent of VoyAgent.

Your ONLY responsibility is understanding the user's travel request.

Extract ONLY the following information:

- destination
- duration_days
- budget
- travelers
- travel_style
- interests
- preferences
- special_requests

DO NOT generate:

- hotels
- flights
- itinerary

Those are handled by other agents.

If some information is missing, make a reasonable assumption.

Return the response according to the provided schema.
""",
        ),
        (
            "human",
            "{input}",
        ),
    ]
)


# ============================================================
# SCHEMAS
# ============================================================

class UserPreferences(BaseModel):

    food_preferences: list[str] = Field(default_factory=list)
    accommodation_type: str | None = None
    transport_preference: str | None = None
    accessibility_needs: list[str] = Field(default_factory=list)


class TripRequirements(BaseModel):

    destination: str
    duration_days: int
    budget: int
    travelers: int
    travel_style: str
    interests: list[str]
    preferences: UserPreferences
    start_date: str |None = None
    special_requests: list[str] = Field(default_factory=list)


# ---------------- HOTEL ----------------

class HotelRecommendation(BaseModel):

    name: str
    location: str
    price_per_night: int
    rating: float
    amenities: list[str]


class HotelRecommendations(BaseModel):

    hotels: list[HotelRecommendation]


# ---------------- FLIGHT ----------------

class FlightRecommendation(BaseModel):

    airline: str
    departure: str
    arrival: str
    price: int
    duration: str


class FlightRecommendations(BaseModel):

    flights: list[FlightRecommendation]


# ---------------- ITINERARY ----------------

class Activity(BaseModel):

    time: str
    title: str
    description: str


class DayPlan(BaseModel):

    day: int
    title: str
    activities: list[Activity]


class DetailedItinerary(BaseModel):

    itinerary: list[DayPlan]


# ---------------- FINAL RESPONSE ----------------

class FinalTravelPlan(BaseModel):

    destination: str
    duration_days: int
    budget: int
    summary: str
    hotels: list[HotelRecommendation]
    flights: list[FlightRecommendation]
    itinerary: list[DayPlan]
    travel_tips: list[str]


# ============================================================
# STATE
# ============================================================

class TravelState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]

    current_agent: str | None

    planner_output: TripRequirements | None

    hotel_output: HotelRecommendations | None

    flight_output: FlightRecommendations | None

    itinerary_output: DetailedItinerary | None

    final_output: FinalTravelPlan | None


# ============================================================
# PLANNER LLM
# ============================================================

planner_llm = llm.with_structured_output(TripRequirements)


# ============================================================
# PLANNER CHAIN (LCEL)
# ============================================================

planner_chain = planner_prompt | planner_llm


# ============================================================
# SUPERVISOR NODE
# ============================================================

def supervisor_node(state: TravelState):

    print("\n========================================")
    print("Supervisor Agent")
    print("========================================")
    print("Delegating task to Planner Agent...\n")

    return {
        "current_agent": "planner",
    }


# ============================================================
# PLANNER NODE
# ============================================================

def planner_node(state: TravelState):

    print("========================================")
    print("Planner Agent")
    print("========================================")
    print("Understanding user requirements...\n")

    user_message = state["messages"][-1].content

    planner_output = planner_chain.invoke(
        {
            "input": user_message,
        }
    )

    return {

        "planner_output": planner_output,

        "messages": [

            HumanMessage(
                content=f"""
Planner extracted the following requirements:

{planner_output.model_dump_json(indent=2)}
"""
            )

        ],

        "current_agent": "planner",

    }


# ============================================================
# MEMORY
# ============================================================

memory = MemorySaver()


# ============================================================
# GRAPH
# ============================================================

graph = StateGraph(TravelState)


# ---------------- Nodes ----------------

graph.add_node(
    "supervisor",
    supervisor_node,
)

graph.add_node(
    "planner",
    planner_node,
)


# ---------------- Edges ----------------

graph.add_edge(
    START,
    "supervisor",
)

graph.add_edge(
    "supervisor",
    "planner",
)

graph.add_edge(
    "planner",
    END,
)


# ============================================================
# COMPILE
# ============================================================

voyagent = graph.compile(
    checkpointer=memory,
)



# ============================================================
# RUN GRAPH
# ============================================================

def run_graph(prompt: str):

    config = {
        "configurable": {
            "thread_id": "user-1",
        }
    }

    result = voyagent.invoke(

        {
            "messages": [
                HumanMessage(content=prompt)
            ]
        },

        config=config,
    )

    return result


# ============================================================
# PRETTY PRINT
# ============================================================

def display_trip_requirements(requirements: TripRequirements):

    print("\n==============================")
    print("TRIP REQUIREMENTS")
    print("==============================")

    print(f"Destination      : {requirements.destination}")
    print(f"Duration         : {requirements.duration_days} Days")
    print(f"Budget           : ₹{requirements.budget}")
    print(f"Travelers        : {requirements.travelers}")
    print(f"Travel Style     : {requirements.travel_style}")

    print("\nInterests")

    for interest in requirements.interests:
        print(f"• {interest}")

    print("\nPreferences")

    print(
        f"Accommodation : {requirements.preferences.accommodation_type}"
    )

    print(
        f"Transport     : {requirements.preferences.transport_preference}"
    )

    print(
        f"Food          : {requirements.preferences.food_preferences}"
    )

    print(
        f"Accessibility : {requirements.preferences.accessibility_needs}"
    )

    print("\nSpecial Requests")

    for request in requirements.special_requests:
        print(f"• {request}")

    print("\n==============================\n")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("      Welcome to VoyAgent AI")
    print("========================================\n")

    while True:

        prompt = input("You : ")

        if prompt.lower() in ["exit", "quit"]:
            break

        result = run_graph(prompt)

        requirements = result["planner_output"]

        display_trip_requirements(requirements)