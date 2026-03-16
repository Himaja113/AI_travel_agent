from langgraph.graph import StateGraph

from workflows.state import TravelState
from agents.destination_agent import destination_agent
from agents.weather_agent import weather_agent
from agents.itinerary_agent import activity_agent


def build_travel_graph():

    graph = StateGraph(TravelState)

    graph.add_node("destination_agent", destination_agent)
    graph.add_node("weather_agent", weather_agent)
    graph.add_node("activity_agent", activity_agent)

    graph.set_entry_point("destination_agent")

    graph.add_edge("destination_agent", "weather_agent")
    graph.add_edge("weather_agent", "activity_agent")

    graph.set_finish_point("activity_agent")

    return graph.compile()