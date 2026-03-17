import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY") # Reusing the same key

def get_routing_data(origin, destination):
    """
    Fetches real road distance and travel time between two points.
    origin/destination can be (lat, lng) or addresses.
    """
    if not GOOGLE_MAPS_API_KEY:
        return None

    url = "https://maps.googleapis.com/maps/api/directions/json"
    
    # Handle tuple/list coordinates
    if isinstance(origin, (tuple, list)):
        origin = f"{origin[0]},{origin[1]}"
    if isinstance(destination, (tuple, list)):
        destination = f"{destination[0]},{destination[1]}"

    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY,
        "mode": "driving" # You can add preference for transit/walking if needed
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "OK":
            route = data["routes"][0]["legs"][0]
            return {
                "distance_km": route["distance"]["value"] / 1000.0,
                "duration_text": route["duration"]["text"],
                "duration_value": route["duration"]["value"], # in seconds
                "polyline": data["routes"][0]["overview_polyline"]["points"]
            }
        else:
            print(f"Directions API Error: {data.get('status')} - {data.get('error_message', 'No message')}")
            return None
    except Exception as e:
        print(f"Error fetching directions: {e}")
        return None
