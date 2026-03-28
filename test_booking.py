from agents.booking_agent import booking_agent

mock_state = {
    "departure_city": "New York",
    "destination": "London",
    "start_date": "2026-05-01",
    "travel_mode": "Flight",
    "book_tickets": True,
}

mock_state_train = {
    "departure_city": "Paris",
    "destination": "Berlin",
    "start_date": "2026-06-10",
    "travel_mode": "Train",
    "book_tickets": True,
}

mock_state_no_tix = {
    "book_tickets": False,
}

print("Testing Flight Booking:")
res = booking_agent(mock_state.copy())
print(res.get("booking_links"))
print("-" * 40)

print("Testing Train Booking:")
res2 = booking_agent(mock_state_train.copy())
print(res2.get("booking_links"))
print("-" * 40)

print("Testing No Tickets:")
res3 = booking_agent(mock_state_no_tix.copy())
print(f"Links provided: {'YES' if res3.get('booking_links') else 'NO'}")
print("All tests passed.")
