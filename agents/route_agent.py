from tools.google_maps_tool import get_routing_data
from geopy.distance import geodesic

def optimize_route(attractions):
    if not attractions or len(attractions) <= 2:
        return attractions, ""

    optimized = [attractions[0]]
    remaining = attractions[1:]
    travel_summary = ""

    while remaining:
        last = optimized[-1]
        best_next = None
        min_dist = float('inf')
        best_route_info = None

        for place in remaining:
            origin = (last["lat"], last["lng"])
            dest = (place["lat"], place["lng"])
            
            route_data = get_routing_data(origin, dest)
            
            if route_data:
                dist = route_data["distance_km"]
            else:
                dist = geodesic(origin, dest).km
            
            if dist < min_dist:
                min_dist = dist
                best_next = place
                best_route_info = route_data

        if best_route_info:
            travel_summary += f"{last['name']} to {best_next['name']}: {best_route_info['distance_km']:.1f} km ({best_route_info['duration_text']})\n"
        else:
            travel_summary += f"{last['name']} to {best_next['name']}: {min_dist:.1f} km (Distance only, time unknown)\n"

        optimized.append(best_next)
        remaining.remove(best_next)

    return optimized, travel_summary

def route_agent(state):
    attractions = state["attractions"]
    optimized, travel_summary = optimize_route(attractions)
    state["attractions"] = optimized
    state["travel_summary"] = travel_summary
    return state