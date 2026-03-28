def get_mock_train_schedules(departure, destination, date):
    # In production, replace this with requests.get() to IRCTC/RapidAPI
    return f"""
    [LIVE MOCK DATA] Available Trains from {departure} to {destination} on {date}:
    1. Vande Bharat Express (Train 22436) - Departs 06:00 AM, Arrives 12:20 PM - Status: Available (125 seats)
    2. Swarn Shatabdi (Train 12004) - Departs 06:10 AM, Arrives 12:40 PM - Status: Waitlist 10
    3. Night Mail (Train 12230) - Departs 10:00 PM (Previous night), Arrives 06:50 AM - Status: Available (42 seats)
    """

def get_mock_flight_schedules(departure, destination, date):
    # In production, replace this with requests.get() to Tequila Kiwi API / Amadeus
    return f"""
    [LIVE MOCK DATA] Available Flights from {departure} to {destination} on {date}:
    1. AirIndia AI-431 - Departs 07:15 AM, Arrives 08:25 AM - Price: $65
    2. IndiGo 6E-2022 - Departs 10:30 AM, Arrives 11:45 AM - Price: $55
    3. Express Airways UK-923 - Departs 05:00 PM, Arrives 06:15 PM - Price: $70
    """

def availability_agent(state):
    print("--- Availability Agent Starting ---")
    
    dep = state.get("departure_city", "Unknown")
    dest = state.get("destination", "Unknown")
    date = state.get("start_date", "Unknown")
    mode = state.get("travel_mode", "Any").lower()
    
    print(f"Fetching live availability for {mode} from {dep} to {dest} on {date}...")
    
    schedules = "Live Transit Schedules (DO NOT HALLUCINATE, ONLY USE THESE IF RELEVANT):\n"
    if mode in ["train", "any"]:
        schedules += get_mock_train_schedules(dep, dest, date) + "\n"
    
    if mode in ["flight", "any"]:
        schedules += get_mock_flight_schedules(dep, dest, date) + "\n"
        
    state["live_transit_schedules"] = schedules
    return state
