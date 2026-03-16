from utils.llm import generate_response

def activity_agent(state):
    if "iterations" not in state:
        state["iterations"] = 0

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

Weather at destination:
{state['weather']}

Top attractions in the destination:
{state['attractions']}

Instructions:
1. Day 1 should include travel from the departure city to the destination.
2. Plan activities around the attractions listed above.
3. Consider weather conditions while planning outdoor activities.
4. Respect the given budget.
5. Include morning, afternoon, and evening activities.

Return a clear day-by-day itinerary.
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
