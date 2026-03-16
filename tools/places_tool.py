import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")


def get_attractions(city):

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": f"tourist attractions in {city}",
        "key": GOOGLE_PLACES_API_KEY
    }

    response = requests.get(url, params=params)
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

# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# def get_attractions(city):

#     url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

#     params = {
#         "query": f"tourist attractions in {city}",
#         "key": GOOGLE_PLACES_API_KEY
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     attractions = []

#     for place in data.get("results", [])[:5]:
#         attractions.append({
#             "name": place["name"],
#             "rating": place.get("rating", "N/A"),
#             "address": place.get("formatted_address")
#         })

#     return attractions