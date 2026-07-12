from langchain_core.prompts import ChatPromptTemplate
from llm.gemini import llm
from schemas.itinerary import DetailedItinerary
from graph.state import TravelState


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


# 2.2 Itinerary LLM
itinerary_llm = llm.with_structured_output(
    DetailedItinerary
)


# 3.2 Itinerary Chain
itinerary_chain = itinerary_prompt | itinerary_llm


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
    }
