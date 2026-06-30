from pydantic import BaseModel


class PlanTripRequest(BaseModel):
    prompt: str


class PlanTripResponse(BaseModel):
    success: bool
    response: str