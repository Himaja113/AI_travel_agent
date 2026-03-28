from utils.llm import generate_response

def activity_agent(state):
    # Increment iterations here so it persists in the state
    state["iterations"] = state.get("iterations", 0) + 1
    
    feedback = state.get("feedback_summary", "None")
    
    print(f"--- Activity Agent Starting (Iteration {state['iterations']}) ---")

    prompt = f"""
You are an expert travel planner.

Trip Details:
Departure City: {state['departure_city']}
Destination: {state['destination']}
Start Date: {state['start_date']}
End Date: {state['end_date']}
Budget: ${state['budget']}
Travelers: {state['travelers']}
Interests: {state['interests']}
Preferred Travel Mode: {state.get('travel_mode', 'Any')}

Weather at destination:
{state['weather']}

Top attractions in the destination:
{state['attractions']}

Real-world travel distances and times between attractions:
{state.get('travel_summary', 'Not available')}

Instructions:
1. Day 1: Plan travel from {state['departure_city']} to {state['destination']}. **You MUST identify and name specific airports** (e.g., Narita Airport, Heathrow Airport) and mention the flight/train numbers if possible.
2. Means of Transport: For EVERY leg of the journey (airport to hotel, hotel to attraction, city to city), **you MUST specify the means of transport** (e.g., "Take the JR Yamanote Line train", "Hire a private cab", "Take the Metro Line 4").
3. Travel Mode (PREFERENCE WITH TRANSPARENT FALLBACKS): The user's preference is "{state.get('travel_mode', 'Any')}".
   - General rule: Use the preferred mode wherever it is realistically available and sensible. If it is NOT available/feasible (due to borders, oceans, extreme duration vs trip dates, or no practical routes), you MAY switch modes, but you MUST:
     (a) state the switch clearly at the very beginning (one short paragraph), and
     (b) explain the reason in plain language.
   - If it is "Bus": Prefer buses/coaches for intercity legs. If the main long-haul leg cannot be done by bus in the given dates (or is not practical), switch to the most realistic mode for that leg (often flight), and disclose it as above.
   - If it is "Train": Prefer trains. If an unavoidable non-train segment exists, use the closest alternative and disclose it.
   - If it is "Flight": Prefer flights for long-haul legs.
   - If it is "Metro/Cab": Treat this as local-in-city preference (still choose a sensible intercity mode).
   - If it is "Any": Choose the most reasonable option
4. Plan activities around the attractions listed above.
5. Consider weather conditions while planning outdoor activities.
6. Respect the given budget of ${state['budget']}. 
   - **Grounding Math**: Use these standard estimates: Flight ($600-$1000), Hotel ($100-$200/night), Food/Local ($50-$100/day).
   - **Recommended Budget**: If "Previous Feedback" suggested a specific minimum budget (e.g., $7000), prioritize that number and explain why it's needed.
   - **Warning**: If the budget is still insufficient, provide a realistic itinerary anyway but **explicitly state at the very beginning**: "⚠️ WARNING: Provided budget of ${state['budget']} is insufficient. A realistic budget for this trip would be approximately $X."
7. Include morning, afternoon, and evening activities.
8. **Include Return Trip**: On the last day ({state['end_date']}), include the travel back from {state['destination']} to {state['departure_city']}, specifying the return airport/station and transport mode.
9. IF there is "Previous Feedback", address it specifically. Use its budget recommendations to achieve a stable, consistent plan.

Return the itinerary clearly, including precise names of stations and transport lines, and end with a **Budget Table** in this format (keep the 3-column layout; use plain numbers in the last column like `1800` or `1142.50` without breaking across lines):
| Category | Details | Cost ($) |
| :--- | :--- | ---: |
| Flights | ... | ... |
| Accommodation | ... | ... |
| Transport | ... | ... |
| Food/Activity | ... | ... |
| **Total** | | **SUM_OF_COSTS** |

Double-check your math! The Total MUST be the exact sum of the items.
"""

    itinerary = generate_response(prompt)
    state["itinerary"] = itinerary
    return state
# from utils.llm import generate_response

# def create_itinerary(data):

#     prompt = f"""
# You are a professional travel planner.

# Create a detailed day-by-day itinerary.

# Departure city: {data['departure_city']}
# Destination: {data['destination']}
# Start date: {data['start_date']}
# End date: {data['end_date']}
# Budget: {data['budget']}
# Number of travelers: {data['travelers']}
# Interests: {data['interests']}

# Rules:
# - Include arrival travel from departure city
# - Respect the budget
# - Include morning, afternoon, evening activities
# - Make travel realistic
# - Include food suggestions

# Return the result clearly formatted by day.
# """

#     itinerary = generate_response(prompt)

#     return itinerary

# /
