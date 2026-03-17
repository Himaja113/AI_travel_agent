import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")


def get_attractions(city):
    if not GOOGLE_PLACES_API_KEY:
        print("Warning: GOOGLE_PLACES_API_KEY not found in environment variables.")
        return []

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": f"tourist attractions in {city}",
        "key": GOOGLE_PLACES_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        attractions = []
        for place in data.get("results", [])[:5]:
            attractions.append({
                "name": place["name"],
                "rating": place.get("rating", "N/A"),
                "address": place.get("formatted_address"),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"]
            })

        return attractions
    except Exception as e:
        print(f"Error fetching attractions from Google Places: {e}")
        return []