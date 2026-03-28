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
    feedback_summary: str
    travel_summary: str
    travel_mode: str
    iterations: int
    book_tickets: bool
    booking_links: str
    live_transit_schedules: str