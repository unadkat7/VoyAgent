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
