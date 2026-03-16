from utils.llm import generate_response


def critic_agent(state):

    prompt = f"""
You are a travel plan reviewer.

Evaluate the following itinerary for feasibility.

Check for:
- unrealistic travel distances
- too many places in a single day
- ignoring weather conditions
- budget violations
- inefficient travel order

Trip plan:
{state["itinerary"]}

Attractions:
{state["attractions"]}

Weather:
{state["weather"]}

Provide:

1. Feasibility score (0–10)
2. Issues detected
3. Suggestions for improvement

Format:
Score:
Issues:
Suggestions:
"""

    critique = generate_response(prompt)

    state["critique"] = critique

    return state