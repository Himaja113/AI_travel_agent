from langgraph.graph import StateGraph, END

from workflows.state import TravelState
from agents.destination_agent import destination_agent
from agents.parallel_gather_agent import parallel_gather_agent
from agents.itinerary_agent import activity_agent
from agents.critic_agent import critic_agent
from agents.booking_agent import booking_agent


def critic_decision(state):
    iterations = state.get("iterations", 0)
    critique = state["critique"].lower()

    print(f"--- Critic Decision for Iteration {iterations} ---")
    
    # stop if score is good
    if "score: 8" in critique or "score: 9" in critique or "score: 10" in critique:
        print("Plan accepted by critic.")
        return "booking"

    # stop if iteration limit reached
    if state["iterations"] >= 3:
        print("Max iterations reached (3). Stopping.")
        return "booking"

    print("Plan rejected. Routing straight back for regeneration using native feedback.")
    return "refine"

def build_travel_graph():

    graph = StateGraph(TravelState)

    graph.add_node("destination_agent", destination_agent)
    graph.add_node("parallel_gather_agent", parallel_gather_agent)
    graph.add_node("activity_agent", activity_agent)
    graph.add_node("critic_agent", critic_agent)
    graph.add_node("booking_agent", booking_agent)

    graph.set_entry_point("destination_agent")

    graph.add_edge("destination_agent", "parallel_gather_agent")
    graph.add_edge("parallel_gather_agent", "activity_agent")
    graph.add_edge("activity_agent", "critic_agent")

    graph.add_conditional_edges(
    "critic_agent",
    critic_decision,
    {
        "booking": "booking_agent",
        "refine": "activity_agent"
    }
)

    graph.add_edge("booking_agent", END)

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