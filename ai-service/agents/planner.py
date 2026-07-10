from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from llm.gemini import llm
from schemas.planner import TripRequirements
from graph.state import TravelState


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

The following 6 fields are REQUIRED for trip planning:
- departure (the city/airport the user is starting their journey from)
- destination
- duration_days
- budget
- travelers
- travel_style

Never guess or assume values. Only extract information explicitly mentioned.

If ANY of the 6 required fields are not explicitly mentioned in the conversation:
1. Leave that field as null.
2. You MUST add the name of every unmentioned required field to the missing_fields list.

For example, if the user does not mention where they are departing from, you MUST include "departure" in missing_fields.

Possible missing fields values:
- departure
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
