from fastapi import APIRouter
from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from graph.builder import voyagent

router = APIRouter()


# ============================================================
# REQUEST SCHEMA
# ============================================================

from typing import Any, Dict, Optional

class PlannerRequest(BaseModel):

    prompt: str
    thread_id: str = "user-1"


class ClarificationPayload(BaseModel):
    missing_fields: list[str]
    question: str


class PlanTripResponse(BaseModel):
    status: str
    thread_id: str
    clarification: Optional[ClarificationPayload] = None
    final_plan: Optional[Dict[str, Any]] = None


# ============================================================
# RUN GRAPH
# ============================================================

def run_graph(
    prompt: str,
    thread_id: str = "user-1",
):

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
# API
# ============================================================

@router.post("/plan-trip", response_model=PlanTripResponse)
def plan_trip(request: PlannerRequest):

    result = run_graph(
        request.prompt,
        request.thread_id,
    )

    # Check if we stopped at clarification or if final_output is missing
    clarification_out = result.get("clarification_output")
    final_out = result.get("final_output")

    if clarification_out or not final_out:
        missing = result["planner_output"].missing_fields if result.get("planner_output") else []
        question = clarification_out.message if clarification_out else (result["messages"][-1].content if result.get("messages") else "Please provide more details for your trip.")
        
        return PlanTripResponse(
            status="clarification_needed",
            thread_id=request.thread_id,
            clarification=ClarificationPayload(
                missing_fields=missing,
                question=question
            ),
            final_plan=None
        )

    # Otherwise trip is completed
    return PlanTripResponse(
        status="completed",
        thread_id=request.thread_id,
        clarification=None,
        final_plan={
            "planner_output": result["planner_output"].model_dump() if result.get("planner_output") else None,
            "hotels": result["hotel_output"].model_dump() if result.get("hotel_output") else None,
            "flights": result["flight_output"].model_dump() if result.get("flight_output") else None,
            "itinerary": result["itinerary_output"].model_dump() if result.get("itinerary_output") else None,
            "final_output": final_out.model_dump() if final_out else None,
        }
    )