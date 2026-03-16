from typing import TypedDict, List


class TravelState(TypedDict):

    departure_city: str
    destination: str
    start_date: str
    end_date: str
    budget: int
    travelers: int
    interests: List[str]

    attractions: list
    weather: dict
    itinerary: str
    critique: str
    iterations: int