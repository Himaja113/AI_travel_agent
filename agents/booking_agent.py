import urllib.parse
from typing import Dict, Any

def get_flight_link(departure: str, destination: str, date: str) -> str:
    dep = urllib.parse.quote_plus(departure)
    dest = urllib.parse.quote_plus(destination)
    # Simple Google Flights search query
    return f"https://www.google.com/travel/flights?q=Flights%20from%20{dep}%20to%20{dest}%20on%20{date}"

def get_train_link(departure: str, destination: str) -> str:
    dep = urllib.parse.quote_plus(departure)
    dest = urllib.parse.quote_plus(destination)
    return f"https://www.thetrainline.com/book/results?origin={dep}&destination={dest}"

def get_bus_link(departure: str, destination: str, date: str) -> str:
    dep = urllib.parse.quote(departure)
    dest = urllib.parse.quote(destination)
    return f"https://www.busbud.com/en/search/{dep}/{dest}/{date}"

def booking_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("--- Booking Agent Starting ---")
    
    if not state.get("book_tickets", False):
        state["booking_links"] = ""
        return state

    dep = state.get("departure_city", "")
    dest = state.get("destination", "")
    date = state.get("start_date", "")
    mode = state.get("travel_mode", "Any").lower()

    links_md = f"### 🎟️ Quick Booking Links for {dest}\n\n"
    links_md += "We've generated these quick search links so you can lock in your dates instantly!\n\n"

    flight_url = get_flight_link(dep, dest, date)
    links_md += f"- ✈️ **[Search Flights on Google Flights]({flight_url})**"
    if mode == "flight": links_md += " *(Your Preference)*"
    links_md += "\n"
    
    train_url = get_train_link(dep, dest)
    links_md += f"- 🚆 **[Search Trains on Trainline]({train_url})**"
    if mode == "train": links_md += " *(Your Preference)*"
    links_md += "\n"
        
    bus_url = get_bus_link(dep, dest, date)
    links_md += f"- 🚌 **[Search Buses on Busbud]({bus_url})**"
    if mode == "bus": links_md += " *(Your Preference)*"
    links_md += "\n"
        
    state["booking_links"] = links_md
    return state
