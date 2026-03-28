from typing import List, TypedDict

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired


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
    book_tickets: NotRequired[bool]
    booking_links: NotRequired[str]
    live_transit_schedules: NotRequired[str]
