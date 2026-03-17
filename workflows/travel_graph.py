from langgraph.graph import StateGraph, END

from workflows.state import TravelState
from agents.destination_agent import destination_agent
from agents.weather_agent import weather_agent
from agents.route_agent import route_agent
from agents.itinerary_agent import activity_agent
from agents.critic_agent import critic_agent
from agents.refiner_agent import refiner_agent


def critic_decision(state):
    iterations = state.get("iterations", 0)
    critique = state["critique"].lower()

    print(f"--- Critic Decision for Iteration {iterations} ---")
    
    # stop if score is good
    if "score: 8" in critique or "score: 9" in critique or "score: 10" in critique:
        print("Plan accepted by critic.")
        return "end"

    # stop if iteration limit reached
    if state["iterations"] >= 4:
        print("Max iterations reached (4). Stopping.")
        return "end"

    print("Plan rejected. Routing to refiner for feedback summary.")
    return "refine"

def build_travel_graph():

    graph = StateGraph(TravelState)

    graph.add_node("destination_agent", destination_agent)
    graph.add_node("weather_agent", weather_agent)
    graph.add_node("route_agent", route_agent)
    graph.add_node("activity_agent", activity_agent)
    graph.add_node("critic_agent", critic_agent)
    graph.add_node("refiner_agent", refiner_agent)

    graph.set_entry_point("destination_agent")

    graph.add_edge("destination_agent", "weather_agent")
    graph.add_edge("weather_agent", "route_agent")
    graph.add_edge("route_agent", "activity_agent")
    graph.add_edge("activity_agent", "critic_agent")

    graph.add_conditional_edges(
    "critic_agent",
    critic_decision,
    {
        "end": END,
        "refine": "refiner_agent"
    }
)

    graph.add_edge("refiner_agent", "activity_agent")

    return graph.compile()
# from langgraph.graph import StateGraph, END

# from workflows.state import TravelState
# from agents.destination_agent import destination_agent
# from agents.weather_agent import weather_agent
# from agents.itinerary_agent import activity_agent
# from agents.critic_agent import critic_agent
# from agents.refiner_agent import refiner_agent
# from agents.route_agent import route_agent  
# def critic_decision(state):

#     critique = state["critique"].lower()

#     if "score: 8" in critique or "score: 9" in critique or "score: 10" in critique:
#         return "end"

#     return "refiner_agent"
# def build_travel_graph():

#     graph = StateGraph(TravelState)

#     graph.add_node("destination_agent", destination_agent)
#     graph.add_node("weather_agent", weather_agent)
#     graph.add_node("route_agent", route_agent)
#     graph.add_node("activity_agent", activity_agent)
#     graph.add_node("critic_agent", critic_agent)
#     graph.add_node("refiner_agent", refiner_agent)

#     graph.set_entry_point("destination_agent")

#     graph.add_edge("destination_agent", "weather_agent")
#     graph.add_edge("weather_agent", "route_agent")
#     graph.add_edge("route_agent", "activity_agent")
#     graph.add_edge("activity_agent", "critic_agent")
#     graph.add_conditional_edges(
#         "critic_agent",
#         critic_decision,
#         {
#             "end": END,
#             "refiner_agent": "refiner_agent"
#         }
#     )

#     graph.add_edge("refiner_agent", END)

#     return graph.compile()