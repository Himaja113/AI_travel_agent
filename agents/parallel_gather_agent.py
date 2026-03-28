import concurrent.futures
from typing import Dict, Any

from agents.weather_agent import weather_agent
from agents.route_agent import route_agent
from agents.availability_agent import availability_agent

def parallel_gather_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("--- Parallel Node: Gathering Weather, Routes, and Availability ---")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Pass a deep-ish copy to avoid dict mutation race conditions
        f1 = executor.submit(weather_agent, dict(state))
        f2 = executor.submit(route_agent, dict(state))
        f3 = executor.submit(availability_agent, dict(state))
        
        s1 = f1.result()
        s2 = f2.result()
        s3 = f3.result()
        
    state["weather"] = s1.get("weather", {})
    state["attractions"] = s2.get("attractions", state.get("attractions"))
    state["travel_summary"] = s2.get("travel_summary", "")
    state["live_transit_schedules"] = s3.get("live_transit_schedules", "")
    
    return state
