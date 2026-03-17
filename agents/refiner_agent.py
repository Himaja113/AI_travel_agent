from utils.llm import generate_response


def refiner_agent(state):
    prompt = f"""
You are a travel expert summarizing feedback for a travel plan.

Current Itinerary:
{state["itinerary"]}

Critic Feedback:
{state["critique"]}

Task:
Identify the top 3-5 specific issues that need fixing and provide clear, actionable suggestions for the travel planner to rewrite the itinerary. 
Do NOT provide the full itinerary. Just provide the summary of needed changes.

Format:
Summary of Issues:
Actionable Suggestions:
"""
    summary = generate_response(prompt)
    
    # Store the summary in the state so the activity agent can use it
    state["feedback_summary"] = summary
    return state