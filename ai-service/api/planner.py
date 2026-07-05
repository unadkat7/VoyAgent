from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from graph.builder import voyagent

router = APIRouter()


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
