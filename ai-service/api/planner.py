from fastapi import APIRouter
from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from graph.builder import voyagent

router = APIRouter()


# ============================================================
# REQUEST SCHEMA
# ============================================================

class PlannerRequest(BaseModel):

    prompt: str
    thread_id: str = "user-1"


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

@router.post("/plan-trip")
def plan_trip(request: PlannerRequest):

    result = run_graph(
        request.prompt,
        request.thread_id,
    )

    return result