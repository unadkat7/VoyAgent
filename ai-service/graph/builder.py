from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graph.state import TravelState
from graph.memory import memory

from agents.supervisor import supervisor_node
from agents.planning import planning_node
from agents.planner import planner_node
from agents.router import (
    router_node,
    route_after_router,
)
from agents.clarification import clarification_node
from agents.hotel import hotel_node
from agents.flight import flight_node
from agents.itinerary import itinerary_node
from agents.composer import response_composer_node


# ============================================================
# GRAPH
# ============================================================

graph = StateGraph(TravelState)

# ============================================================
# NODES
# ============================================================

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
    planning_node,
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

# ============================================================
# EDGES
# ============================================================

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

# ---------------- Planning Pipeline ----------------

graph.add_edge(
    "planning",
    "hotel",
)

graph.add_edge(
    "hotel",
    "flight",
)

graph.add_edge(
    "flight",
    "itinerary",
)

graph.add_edge(
    "itinerary",
    "composer",
)

graph.add_edge(
    "composer",
    END,
)

# ============================================================
# COMPILE
# ============================================================

voyagent = graph.compile(
    checkpointer=memory
)