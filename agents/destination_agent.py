from tools.places_tool import get_attractions

def destination_agent(state):

    destination = state["destination"]
    interests = state.get("interests", [])

    attractions = get_attractions(destination, interests)
    
    # Tag attractions with city name for map coloring
    for attr in attractions:
        attr["city"] = destination

    state["attractions"] = attractions

    return state