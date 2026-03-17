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
3. Travel Mode: Respect the user's preference for "{state.get('travel_mode', 'Any')}" where feasible, especially for domestic travel.
4. Plan activities around the attractions listed above.
5. Consider weather conditions while planning outdoor activities.
6. Respect the given budget of ${state['budget']}. **If this budget is clearly insufficient** for the requested duration, destination, and essentials (like flights), provide a realistic itinerary anyway but **explicitly state at the very beginning**: "⚠️ WARNING: Provided budget of ${state['budget']} is insufficient. A realistic budget for this trip would be approximately $X."
7. Include morning, afternoon, and evening activities.
8. **Include Return Trip**: On the last day ({state['end_date']}), include the travel back from {state['destination']} to {state['departure_city']}, specifying the return airport/station and transport mode.
9. IF there is "Previous Feedback", address it specifically.

Return the itinerary clearly, including precise names of stations and transport lines, and end with a **Budget Table** in this format:
| Category | Details | Cost ($) |
| :--- | :--- | :--- |
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
