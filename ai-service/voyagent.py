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
    AIMessage,
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

Your ONLY responsibility is understanding the user's travel requirements.

The input is the COMPLETE conversation between the user and the assistant.

Your task is to combine all information from the conversation
and extract the latest travel requirements.

Never guess.

Never assume.

Only extract information explicitly mentioned.

If information is missing,
leave the field as null.

Populate the missing_fields list.

Possible missing fields:

- destination
- duration_days
- budget
- travelers
- travel_style

Return ONLY the TripRequirements object.

Do NOT generate:

- hotels
- flights
- itinerary
- travel recommendations
"""
        ),
        (
            "human",
            "{conversation}"
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


class ClarificationResponse(BaseModel):

    questions: list[str] = Field(default_factory=list)

    message: str


class TripRequirements(BaseModel):

    destination: str | None = None

    duration_days: int | None = None

    budget: int | None = None

    travelers: int | None = None

    travel_style: str | None = None

    interests: list[str] = Field(default_factory=list)

    preferences: UserPreferences = Field(
        default_factory=UserPreferences
    )

    start_date: str | None = None

    special_requests: list[str] = Field(default_factory=list)

    missing_fields: list[str] = Field(default_factory=list)


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


# ============================================================
# LLMs
# ============================================================

planner_llm = llm.with_structured_output(
    TripRequirements
)


# ============================================================
# LCEL CHAINS
# ============================================================

planner_chain = planner_prompt | planner_llm


# ============================================================
# SUPERVISOR NODE
# ============================================================

def supervisor_node(state: TravelState):

    print("\n========================================")
    print("Supervisor Agent")
    print("========================================")
    print("Starting travel planning workflow...\n")

    return {
        "current_agent": "planner"
    }


# ============================================================
# PLANNER NODE
# ============================================================

def planner_node(state: TravelState):

    print("\n========================================")
    print("Planner Agent")
    print("========================================")

    # Build the entire conversation
    conversation = ""

    for message in state["messages"]:

        if isinstance(message, HumanMessage):
            conversation += f"User: {message.content}\n"

        elif isinstance(message, AIMessage):
            conversation += f"Assistant: {message.content}\n"

    print("Analyzing complete conversation...\n")

    planner_output = planner_chain.invoke(
        {
            "conversation": conversation
        }
    )

    print("Planner Output:\n")
    print(planner_output.model_dump_json(indent=2))

    return {

        "planner_output": planner_output,

        "current_agent": "planner"

    }


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: TravelState):

    planner = state["planner_output"]

    print("\n========================================")
    print("Router Agent")
    print("========================================")

    if planner.missing_fields:

        print("Missing information detected.")

        return {
            "current_agent": "clarification"
        }

    print("All required information collected.")

    return {
        "current_agent": "planning"
    }


# ============================================================
# CLARIFICATION AGENT
# ============================================================

def clarification_node(state: TravelState):

    planner = state["planner_output"]

    questions = {

        "destination":
            "Which destination would you like to visit?",

        "duration_days":
            "How many days will your trip be?",

        "budget":
            "What's your approximate budget?",

        "travelers":
            "How many travelers are going?",

        "travel_style":
            "What kind of trip are you looking for? (Luxury, Budget, Adventure, Family...)"

    }

    response = (
        "Before I continue planning your trip, "
        "I need a little more information.\n\n"
    )

    for field in planner.missing_fields:

        response += f"• {questions[field]}\n"

    print("\n========================================")
    print("Clarification Agent")
    print("========================================")
    print(response)

    return {

        "messages": [
            AIMessage(content=response)
        ],

        "current_agent": "clarification"

    }


# ============================================================
# PLANNING PIPELINE
# ============================================================

def planning_pipeline_node(state: TravelState):

    print("\n========================================")
    print("Planning Pipeline")
    print("========================================")

    print("Planner has gathered all the required information.")

    print("\nNext Version:")

    print("→ Hotel Agent")
    print("→ Flight Agent")
    print("→ Itinerary Agent")

    return {

        "current_agent": "planning"

    }


# ============================================================
# ROUTING FUNCTION
# ============================================================

def route_after_router(state: TravelState):

    if state["current_agent"] == "clarification":
        return "clarification"

    return "planning"


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

graph.add_node(
    "router",
    router_node,
)

graph.add_node(
    "clarification",
    clarification_node,
)

graph.add_node(
    "planning",
    planning_pipeline_node,
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
    "router",
)

graph.add_conditional_edges(
    "router",
    route_after_router,
    {
        "clarification": "clarification",
        "planning": "planning",
    },
)

graph.add_edge(
    "clarification",
    END,
)

graph.add_edge(
    "planning",
    END,
)

# ============================================================
# COMPILE
# ============================================================

voyagent = graph.compile(
    checkpointer=memory
)


# ============================================================
# RUN GRAPH
# ============================================================

# ============================================================
# RUN GRAPH
# ============================================================

def run_graph(prompt: str, thread_id: str = "user-1"):

    config = {
        "configurable": {
            "thread_id": thread_id
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
# DISPLAY
# ============================================================

def display_trip_requirements(
    requirements: TripRequirements,
):

    print("\n==============================")
    print("Trip Requirements")
    print("==============================")

    print(f"Destination   : {requirements.destination}")
    print(f"Duration      : {requirements.duration_days}")
    print(f"Budget        : {requirements.budget}")
    print(f"Travelers     : {requirements.travelers}")
    print(f"Travel Style  : {requirements.travel_style}")

    print("\nInterests")

    if requirements.interests:

        for interest in requirements.interests:

            print(f"• {interest}")

    else:

        print("None")

    print("\nMissing Fields")

    if requirements.missing_fields:

        for field in requirements.missing_fields:

            print(f"• {field}")

    else:

        print("None")

    print()

# ============================================================
# MAIN
# ============================================================

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

            print("\nVoyAgent\n")

            print(result["messages"][-1].content)

        else:

            print("\nPlanning Pipeline Ready\n")

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