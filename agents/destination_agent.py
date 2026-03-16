from tools.places_tool import get_attractions

def destination_agent(state):

    destination = state["destination"]

    attractions = get_attractions(destination)

    state["attractions"] = attractions

    return state