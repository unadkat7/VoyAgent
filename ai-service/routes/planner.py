from fastapi import APIRouter, HTTPException

from schemas.planner_schema import (
    PlanTripRequest,
    PlanTripResponse,
)

from services.gemini import generate_response

router = APIRouter(
    prefix="/planner",
    tags=["Trip Planner"],
)


@router.post(
    "/plan-trip",
    response_model=PlanTripResponse,
)
def plan_trip(request: PlanTripRequest):
    try:
        response = generate_response(request.prompt)

        return PlanTripResponse(
            success=True,
            response=response,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )