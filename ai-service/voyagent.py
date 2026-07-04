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

    price_per_night: float

    currency: str

    booking_url: str | None

    rating: float

    amenities: list[str]


class HotelRecommendations(BaseModel):

    hotels: list[HotelRecommendation]


# ---------------- FLIGHT ----------------

class FlightRecommendation(BaseModel):

    airline: str

    flight_number: str

    departure_airport: str

    arrival_airport: str

    departure_time: str | None

    arrival_time: str | None

    duration: str

    price: float

    currency: str

    stops: int


class FlightRecommendations(BaseModel):

    flights: list[FlightRecommendation]


# ---------------- ITINERARY ----------------

class Activity(BaseModel):

    time: str

    title: str

    description: str

    location: str

    estimated_cost: float

    notes: str | None = None


class DayPlan(BaseModel):

    day: int

    title: str

    activities: list[Activity]


class DetailedItinerary(BaseModel):

    itinerary: list[DayPlan]

# ---------------- FINAL RESPONSE ----------------

class FinalTravelPlan(BaseModel):

    summary: str

    destination: str

    duration_days: int

    budget: int

    travelers: int

    travel_style: str

    hotels: list[HotelRecommendation]

    flights: list[FlightRecommendation]

    itinerary: list[DayPlan]

    important_tips: list[str]


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
        "current_agent": "hotel"
    }


# ============================================================
# CLARIFICATION AGENT
# ============================================================

def clarification_node(state: TravelState):

    planner = state["planner_output"]

    question_map = {
        "destination": "Which destination would you like to visit?",
        "duration_days": "How many days is your trip?",
        "budget": "What's your approximate budget?",
        "travelers": "How many travelers are going?",
        "travel_style": "What type of trip do you want (Luxury, Budget, Adventure...)?"
    }

    questions = [
        question_map[field]
        for field in planner.missing_fields
    ]

    message = (
        "Before I continue planning your trip, "
        "I need a little more information:\n\n"
    )

    for question in questions:
        message += f"• {question}\n"

    clarification = ClarificationResponse(
        questions=questions,
        message=message,
    )

    return {
        "clarification_output": clarification,
        "messages": [
            AIMessage(content=message)
        ],
        "current_agent": "clarification",
    }



# ============================================================
# ROUTING FUNCTION
# ============================================================

def route_after_router(state: TravelState):

    if state["current_agent"] == "clarification":
        return "clarification"

    return "hotel"


# Hotel Agent



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

# 1.2 Itinerary Prompt
itinerary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the Itinerary Agent of VoyAgent.

Your ONLY responsibility is creating a day-wise travel itinerary.

You will receive TripRequirements.

Generate a detailed itinerary.

Each day should include:

- Morning
- Afternoon
- Evening

Recommend attractions that match:

- destination
- duration
- travel style
- interests

Keep the itinerary practical.

Do NOT recommend hotels.

Do NOT recommend flights.

Return ONLY the DetailedItinerary schema.
"""
        ),

        (
            "human",
            "{planner_output}"
        ),
    ]
)

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

# 2. Hotel LLM

hotel_llm = llm.with_structured_output(
    HotelRecommendations
)

# 2.1 Flight LLM
flight_llm = llm.with_structured_output(
    FlightRecommendations
)

# 2.2 Itinerary LLM
itinerary_llm = llm.with_structured_output(
    DetailedItinerary
)

#composer llm
composer_llm = llm.with_structured_output(
    FinalTravelPlan
)

# 3. Hotel Chain
hotel_chain = hotel_prompt | hotel_llm

# 3.1 Flight Chain
flight_chain = flight_prompt | flight_llm

# 3.2 Itinerary Chain
itinerary_chain = itinerary_prompt | itinerary_llm

composer_chain = composer_prompt | composer_llm


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

# 4.2 Itinerary Node
def itinerary_node(state: TravelState):

    print("\n===================================")
    print("Itinerary Agent")
    print("===================================\n")

    planner = state["planner_output"]

    itinerary_output = itinerary_chain.invoke(
        {
            "planner_output":
            planner.model_dump_json(indent=2)
        }
    )


    print("\nGenerated Itinerary\n")

    for day in itinerary_output.itinerary:

        print(f"Day {day.day} : {day.title}")

    return {

        "itinerary_output": itinerary_output,

        "current_agent":"itinerary"

    }

def response_composer_node(state: TravelState):

    print("\n===================================")
    print("Response Composer Agent")
    print("===================================\n")

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

    print("\nFinal Travel Plan Created\n")

    return {

        "final_output": final_output,

        "current_agent": "composer"

    }


def planning_node(state: TravelState):

    print("\n===================================")
    print("Planning Coordinator")
    print("===================================\n")

    print("Dispatching specialist agents...\n")

    return {}

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
    "planning",
    planning_node
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
    "hotel",
    hotel_node,
)

graph.add_node(
    "flight",
    flight_node,
)

graph.add_node(
    "itinerary",
    itinerary_node,
)

graph.add_node(
    "composer",
    response_composer_node,
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

graph.add_edge(
    "planning",
    "hotel"
)

graph.add_edge(
    "planning",
    "flight"
)

graph.add_edge(
    "planning",
    "itinerary"
)

graph.add_edge(
    "clarification",
    END,
)

graph.add_conditional_edges(
    "router",
    route_after_router,
    {
        "clarification":"clarification",
        "planning":"planning"
    }
)

graph.add_edge(
    "composer",
    END
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

    print("\n========================================")
    print("        TRIP REQUIREMENTS")
    print("========================================")

    print(f"Destination     : {requirements.destination or 'Not Provided'}")
    print(f"Duration        : {requirements.duration_days or 'Not Provided'}")
    print(f"Budget          : {requirements.budget or 'Not Provided'}")
    print(f"Travelers       : {requirements.travelers or 'Not Provided'}")
    print(f"Travel Style    : {requirements.travel_style or 'Not Provided'}")
    print(f"Start Date      : {requirements.start_date or 'Not Provided'}")

    # ---------------- Interests ----------------

    print("\nInterests")
    print("----------------------------------------")

    if requirements.interests:
        for interest in requirements.interests:
            print(f"• {interest}")
    else:
        print("None")

    # ---------------- Preferences ----------------

    print("\nUser Preferences")
    print("----------------------------------------")

    prefs = requirements.preferences

    print(
        f"Accommodation : {prefs.accommodation_type or 'Not Provided'}"
    )

    print(
        f"Transport     : {prefs.transport_preference or 'Not Provided'}"
    )

    print("Food Preferences")

    if prefs.food_preferences:
        for food in prefs.food_preferences:
            print(f"• {food}")
    else:
        print("None")

    print("\nAccessibility Needs")

    if prefs.accessibility_needs:
        for need in prefs.accessibility_needs:
            print(f"• {need}")
    else:
        print("None")

    # ---------------- Special Requests ----------------

    print("\nSpecial Requests")
    print("----------------------------------------")

    if requirements.special_requests:
        for request in requirements.special_requests:
            print(f"• {request}")
    else:
        print("None")

    # ---------------- Missing Fields ----------------

    print("\nMissing Fields")
    print("----------------------------------------")

    if requirements.missing_fields:
        for field in requirements.missing_fields:
            print(f"• {field}")
    else:
        print("None")

    print("\n========================================\n")

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

            print("\n==============================")
            print("HOTEL RECOMMENDATIONS")
            print("==============================")

            hotels = result["hotel_output"].hotels

            for i, hotel in enumerate(hotels, start=1):

                print(f"\nHotel {i}")

                print(f"Name       : {hotel.name}")
                print(f"Location   : {hotel.location}")
                print(
                   f"Price : {hotel.currency} {hotel.price_per_night}/night")
                print(f"Rating     : {hotel.rating}")

                print("Amenities")

                for amenity in hotel.amenities:
                    print(f"• {amenity}")
            

            if result.get("flight_output"):

                print("\n==============================")
                print("FLIGHT RECOMMENDATIONS")
                print("==============================")

                for flight in result["flight_output"].flights:

                    print(f"\n✈ Airline      : {flight.airline}")
                    print(f"Flight No.     : {flight.flight_number}")
                    print(f"From           : {flight.departure_airport}")
                    print(f"To             : {flight.arrival_airport}")
                    print(f"Departure      : {flight.departure_time}")
                    print(f"Arrival        : {flight.arrival_time}")
                    print(f"Duration       : {flight.duration}")
                    print(f"Stops          : {flight.stops}")
                    print(f"Price          : {flight.currency} {flight.price}")

            if result.get("itinerary_output"):

                print("\n==============================")
                print("ITINERARY")
                print("==============================")

                for day in result["itinerary_output"].itinerary:

                    print(f"\n📅 Day {day.day}: {day.title}")

                    for activity in day.activities:

                        print(f"\n🕒 {activity.time}")
                        print(f"Activity : {activity.title}")
                        print(f"Location : {activity.location}")
                        print(f"Description : {activity.description}")
                        print(f"Estimated Cost : {activity.estimated_cost}")

                        if activity.notes:
                            print(f"Notes : {activity.notes}")
            
            if result.get("final_output"):

                final = result["final_output"]

                print("\n========================================")
                print("FINAL TRAVEL PLAN")
                print("========================================")

                print(final.summary)

                print("\nTravel Tips")

                for tip in final.important_tips:

                    print(f"• {tip}")
