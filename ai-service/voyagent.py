# ============================
# Imports
# ============================

from dotenv import load_dotenv

from typing import TypedDict, Annotated

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# ============================
# System Prompt
# ============================

SYSTEM_PROMPT = """
You are VoyAgent's Planner Agent.

Your ONLY responsibility is travel planning.

Generate detailed, practical and well-structured travel itineraries.

If the user asks something unrelated to travel,
politely tell them that you only help with travel planning.
"""

# ============================
# LLM
# ============================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

# ============================
# State
# ============================

class TravelState(TypedDict):

    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Current active agent
    current_agent: str | None

    # Planner output
    trip_plan: dict | None


# ============================
# Supervisor Node
# ============================

def supervisor_node(state: TravelState):

    print("\n[Supervisor] Delegating task to Planner Agent...\n")

    return {
        "current_agent": "planner"
    }


# ============================
# Planner Node
# ============================

def planner_node(state: TravelState):

    print("[Planner] Generating itinerary...\n")

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm.invoke(messages)

    return {
        "messages": [
            AIMessage(content=response.content)
        ],

        "trip_plan": {
            "response": response.content
        }
    }


# ============================
# Memory
# ============================

memory = MemorySaver()

# ============================
# Graph
# ============================

graph = StateGraph(TravelState)

graph.add_node("supervisor", supervisor_node)
graph.add_node("planner", planner_node)

graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "planner")
graph.add_edge("planner", END)

voyagent = graph.compile(
    checkpointer=memory
)

# ============================
# Run Helper
# ============================

def run_graph(prompt: str):

    config = {
        "configurable": {
            "thread_id": "user-1"
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


# ============================
# Test
# ============================

if __name__ == "__main__":

    while True:

        user_input = input("\nYou : ")

        if user_input.lower() == "exit":
            break

        response = run_graph(user_input)

        print("\nVoyAgent:\n")
        print(response["trip_plan"]["response"])