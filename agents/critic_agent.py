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
   - **Remaining Suggestions**: Do NOT penalize the budget if the core "Total" is lower than the user's budget, even if "Remaining Budget Suggestions" are listed at the bottom.
- missing or vague transportation details (Must specify train lines, metro, or mode of travel. "Take a taxi" is fine if it specifies to/from where)
- missing specific airport OR train/bus station names for arrival/departure (depending on their travel mode)
- penalizing long travel times IF it matches the user's preferred mode (Do NOT dock points for a 7-hour train ride if that was the explicitly requested mode of transport)
- ending the trip early (The itinerary MUST exactly span from {state['start_date']} to {state['end_date']}. Count the days and penalize heavily if it cuts the trip short!)
- missing explicit return trip to {state['departure_city']} on the exact final date ({state['end_date']})

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
2. Actionable Feedback: If the score is 7 or below, explicitly list the top 3-5 specific instructions to fix the itinerary (e.g. "Change the Day 2 hotel to a cheaper one to save $300"). If the score is 8 or above, just write "None".

Format:
Score: [number]
Feedback: [your actionable instructions]
"""

    critique = generate_response(prompt)
    
    state["critique"] = critique
    state["feedback_summary"] = critique

    return state