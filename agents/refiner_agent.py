from utils.llm import generate_response


def refiner_agent(state):

    prompt = f"""
You are improving a travel itinerary based on critic feedback.

Original itinerary:
{state["itinerary"]}

Critic feedback:
{state["critique"]}

Rewrite the itinerary so that:
- travel distances are realistic
- activities per day are manageable
- travel order is efficient
- budget constraints are respected

Return the FULL revised itinerary.
"""

    improved_plan = generate_response(prompt)

    # IMPORTANT: overwrite itinerary
    state["itinerary"] = improved_plan

    return state