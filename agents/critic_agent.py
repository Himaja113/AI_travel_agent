from utils.llm import generate_response


def critic_agent(state):

    prompt = f"""
You are a travel plan reviewer.

Evaluate the following itinerary for feasibility.

Check for:
- unrealistic travel distances (use the "Travel Summary" below for ground truth)
- too many places in a single day
- ignoring weather conditions
- budget violations (YOU MUST MANUALLY SUM THE COSTS IN THE ITINERARY AND FLAG ANY MATH ERRORS). 
   - **Grounding Math**: Use these standard estimates for Japan: Flights ($800-$1200), Hotels ($150/night), Daily Food/Transport ($80/day). 
   - **Consistency**: If you suggested a budget in a previous iteration (e.g., $7000), do NOT increase it further unless the itinerary changed significantly.
- missing or vague transportation details (Must specify train lines, metro, or mode of travel)
- missing specific airport names for arrival/departure
- missing return trip to {state['departure_city']} on the final day

Itinerary:
{state["itinerary"]}

Attractions Data:
{state["attractions"]}

Travel Summary (Ground Truth distances):
{state.get("travel_summary", "Not available")}

Weather:
{state["weather"]}

Provide:

1. Feasibility score (0–10)
2. Issues detected (Be specific about math errors or travel time hallucinations)
3. Suggestions for improvement

Format:
Score:
Issues:
Suggestions:
"""

    critique = generate_response(prompt)

    state["critique"] = critique

    return state