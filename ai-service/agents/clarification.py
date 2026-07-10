from langchain_core.messages import AIMessage
from schemas.planner import ClarificationResponse
from graph.state import TravelState


# ============================================================
# CLARIFICATION AGENT
# ============================================================

def clarification_node(state: TravelState):

    planner = state["planner_output"]

    question_map = {
        "departure": "Where will you be departing from (your city or airport)?",
        "destination": "Which destination would you like to visit?",
        "duration_days": "How many days is your trip?",
        "budget": "What's your approximate budget?",
        "travelers": "How many travelers are going?",
        "travel_style": "What type of trip do you want (Luxury, Budget, Adventure...)?"
    }

    questions = [
        question_map.get(field, f"Please specify {field}.")
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
