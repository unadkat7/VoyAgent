from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from llm.gemini import llm
from schemas.critic import ValidationResult
from schemas.planner import ClarificationResponse
from graph.state import TravelState

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are the Critic Agent for VoyAgent. Review the total price of the Proposed Hotels and Flights against the User's Total Budget.
        
        If the sum of the cheapest flight and cheapest hotel exceeds the total budget, the trip is impossible.
        Set is_valid to False, and in 'critique', write a polite message asking the user if they want to increase their budget or change their dates.
        If the budget is fine, set is_valid to True.
        """
    ),
    (
        "human",
        """
        User Budget: {budget}
        
        Proposed Hotel: {hotel_output}
        Proposed Flight: {flight_output}
        """
    )
])

critic_llm = llm.with_structured_output(ValidationResult)
critic_chain = critic_prompt | critic_llm

def critic_node(state: TravelState):
    planner = state.get("planner_output")
    hotels = state.get("hotel_output")
    flights = state.get("flight_output")

    validation = critic_chain.invoke({
        "budget": planner.budget if planner else "Unknown",
        "hotel_output": hotels.model_dump_json() if hotels else "",
        "flight_output": flights.model_dump_json() if flights else "",
    })

    if not validation.is_valid:
        # Trigger Human-in-the-Loop!
        clarification = ClarificationResponse(
            questions=["Budget constraint violated"],
            message=validation.critique
        )
        return {
            "critic_output": validation,
            "clarification_output": clarification,
            "messages": [AIMessage(content=validation.critique)],
            "current_agent": "critic"
        }

    return {
        "critic_output": validation,
        "current_agent": "critic"
    }
