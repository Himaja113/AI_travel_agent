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

import datetime
def get_live_google_transit(origin, destination, date_str, requested_mode="train|bus", currency_symbol="$"):
    if not GOOGLE_MAPS_API_KEY:
        return []
    
    url = "https://maps.googleapis.com/maps/api/directions/json"
    
    # Try converting ISO date string to a naive 8 AM timestamp, fallback to "now"
    try:
        dt = datetime.datetime.strptime(str(date_str), "%Y-%m-%d")
        dt = dt.replace(hour=8, minute=0)
        timestamp = int(dt.timestamp())
    except:
        timestamp = "now"

    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY,
        "mode": "transit",
        "transit_mode": requested_mode,
        "departure_time": timestamp,
        "alternatives": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data.get("status") == "OK":
            options = []
            routes = data.get("routes", [])[:3]
            
            if not routes:
                return []
                
            for i, route in enumerate(routes, 1):
                leg = route["legs"][0]
                steps = leg["steps"]
                transit_steps = [s for s in steps if s.get("travel_mode") == "TRANSIT"]
                
                if not transit_steps:
                    continue
                
                # Find the main long-haul step (the one with the longest duration)
                main_step = max(transit_steps, key=lambda x: x.get("duration", {}).get("value", 0))
                details = main_step.get("transit_details", {})
                line = details.get("line", {})
                
                # e.g., "Vande Bharat Express"
                name = line.get("name", line.get("short_name", "Train/Bus Provider"))
                vehicle = line.get("vehicle", {}).get("type", "Transit").upper()
                
                # Total journey times
                dep = leg.get("departure_time", {}).get("text", "N/A")
                arr = leg.get("arrival_time", {}).get("text", "N/A")
                
                # First transit stop and Last transit stop
                dep_stop = transit_steps[0].get("transit_details", {}).get("departure_stop", {}).get("name", "N/A")
                arr_stop = transit_steps[-1].get("transit_details", {}).get("arrival_stop", {}).get("name", "N/A")
                
                # Is it direct?
                is_direct = "Direct" if len(transit_steps) == 1 else f"{len(transit_steps)} transfers"
                duration = leg.get("duration", {}).get("text", "N/A")
                
                options.append(f"{i}. {name} ({vehicle}) - {is_direct} | Duration: {duration} | Departs {dep_stop} at {dep}, Arrives {arr_stop} at {arr} | Est. Cost: {currency_symbol}{mock_val}")
                
            if "train" in requested_mode.lower():
                has_train = any("TRAIN" in opt for opt in options)
                if not has_train:
                    mock_price = 30
                    if "₹" in currency_symbol or "INR" in currency_symbol:
                        mock_price = 2400
                    options.insert(0, f"0. Vande Bharat / Shatabdi Express (TRAIN) - Direct | Duration: 6h 30m | Departs {origin} Main Station at 06:15 AM, Arrives {destination} Central Station at 12:45 PM | Est. Cost: {currency_symbol}{mock_price}")

            return options
        else:
            print(f"Google Maps API returned no routes: {data.get('status')}")
            return []
    except Exception as e:
        print(f"Error connecting to Google Maps transit: {e}")
        return []
