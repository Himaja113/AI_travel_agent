import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")


def get_attractions(city, interests=[]):
    if not GOOGLE_PLACES_API_KEY:
        print("Warning: GOOGLE_PLACES_API_KEY not found in environment variables.")
        return []

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    # We will perform multiple queries to get a diversified list
    queries = [f"top tourist attractions in {city}"]
    if interests:
        for interest in interests:
            queries.append(f"{interest} spots in {city}")

    all_attractions = []
    seen_names = set()

    for query in queries:
        params = {
            "query": query,
            "key": GOOGLE_PLACES_API_KEY
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Take top 3 for each query to keep data manageable but diverse
            for place in data.get("results", [])[:3]:
                name = place["name"]
                if name not in seen_names:
                    all_attractions.append({
                        "name": name,
                        "rating": place.get("rating", "N/A"),
                        "address": place.get("formatted_address"),
                        "lat": place["geometry"]["location"]["lat"],
                        "lng": place["geometry"]["location"]["lng"]
                    })
                    seen_names.add(name)

        except Exception as e:
            print(f"Error fetching attractions for query '{query}': {e}")

    return all_attractions