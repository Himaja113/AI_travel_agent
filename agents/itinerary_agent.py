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

Verified Live Transit Schedules & Availability:
{state.get('live_transit_schedules', 'No live schedules found.')}

Instructions:
1. Day 1: Plan travel from {state['departure_city']} to {state['destination']}. **You MUST use the exact options provided in the "Verified Live Transit Schedules" section above**. DO NOT invent or guess specific flight/train numbers (e.g. Train 12039) or exact departure minutes. If there are NO schedules provided in the verified block, use realistic broad time blocks like "Morning Departure" or "Late Afternoon". Remind the user to check the "🎟️ Bookings" tab for live booking.
2. Means of Transport: For EVERY leg of the journey (airport to hotel, hotel to attraction, city to city), **specify the means of transport** (e.g., "Take a regional train", "Hire a private cab", "Take the Metro"). Do not hallucinate exact local bus/train line numbers if you aren't certain.
3. Travel Mode Rules for LONG-HAUL vs LOCAL:
   - **Long-Haul (City to City)**: The user requested mode is THIS: "{state.get('travel_mode', 'Any')}".
     **CRITICAL COMMAND**: You MUST build the main long-haul journey using the exact requested mode if it is physically possible by land (no oceans/closed borders), NO MATTER HOW LONG IT TAKES. Do NOT switch to a flight merely because a train/bus takes too long.
     - If they chose **Train** or **Bus**, build the timeline utilizing that mode. Add a polite warning at the top estimating the extremely long travel time, stating that it compromises the number of attractions visited, and mentioning that a Flight would be faster/cheaper as a pure suggestion. But STILL generate the actual day-by-day steps based on their Train/Bus choice.
     - If no direct trains/buses exist, strictly use connecting trains/buses and estimate the cost.
   - **Local Travel (Within Destination City)**: Do NOT force the user's Long-Haul preference for local city transit. Always select the most feasible local option (e.g., Metro, Cab, walking) depending on real-world distance and availability inside the city limits.
   - **If "Any"**: Choose the most reasonable long-haul option that is both cost-efficient and time-efficient.
4. **Strict Trip Duration Enforcement:** You MUST generate a day-by-day plan that exactly spans from the Start Date ({state['start_date']}) to the End Date ({state['end_date']}). Do NOT cut the trip short!
   - If you run out of provided attractions in '{state['destination']}' to fill the days, you MUST dynamically suggest day trips to neighboring cities within the same state, hidden regional gems, or relaxing leisure days to fill the timeline.
5. **Accommodation/Hotel Suggestions:** Do NOT just vaguely say "the hotel". On Day 1, you MUST suggest a specific popular neighborhood or a specific highly-rated hotel name in '{state['destination']}' that matches the traveler's budget. Explicitly name it when they check in (e.g., "Check-in at the Taj West End" or "Check-in at a boutique hotel in Indiranagar").
6. Consider weather conditions while planning outdoor activities.
6. Respect the maximum given budget of ${state['budget']}. 
   - **Grounding Math**: Use standard estimates: Flight ($600-$1000), Hotel ($100-$200/night), Food/Local ($50-$100/day). Note that domestic trains in places like India are much cheaper. Use realistic local costs based on the region.
   - **Under Budget is Perfect**: Do NOT inflate prices or add unnecessary expenses (like switching from train to flight) merely to reach the user's budget! If your calculated total is lower than the user's budget, do NOT issue any budget warnings.
   - **Over Budget Warning**: ONLY if the realistic *minimum* cost of the trip is strictly greater than the user's budget, add this explicitly at the very beginning: "⚠️ WARNING: Provided budget of ${state['budget']} is insufficient. A realistic budget would be approximately $X."
   - **Remaining Budget Suggestions**: If the final total is comfortably below the user's budget, add a section at the very end (below the Budget Table) suggesting 1-2 famous shopping areas or premium activities in the destination to utilize their remaining budget. Only recommend things genuinely famous in that area.
7. Include morning, afternoon, and evening activities.
8. **Include Return Trip**: On the final day ({state['end_date']}), you MUST explicitly generate the return journey back to {state['departure_city']}, specifying the exact return airport/station and the final transportation mode. Do not forget this step.
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
