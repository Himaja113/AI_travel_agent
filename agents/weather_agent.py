from tools.weather_tool import get_weather

def weather_agent(state):

    destination = state["destination"]

    weather = get_weather(destination)

    state["weather"] = weather

    return state