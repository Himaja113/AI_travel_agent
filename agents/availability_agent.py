import os
import requests
import re
from utils.llm import generate_response
from tools.google_maps_tool import get_live_google_transit

def get_iata_code(city):
    prompt = f"What is the standard 3-letter IATA airport code for the city of {city}? Return ONLY the 3 uppercase letters, nothing else."
    response = generate_response(prompt).strip()
    match = re.search(r'[A-Z]{3}', response)
    return match.group(0) if match else "DEL"

def get_station_code(city):
    if city.lower() == "delhi":
        return "NDLS"
    prompt = f"What is the standard main Indian Railways station code for the city of {city}? Return ONLY the 2-4 uppercase letters, nothing else (e.g. NDLS for New Delhi, LKO for Lucknow)."
    response = generate_response(prompt).strip()
    match = re.search(r'[A-Z]{2,4}', response)
    return match.group(0) if match else "NDLS"

def get_live_flight_schedules(departure, destination, date, currency_code, currency_symbol):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return ""
    
    dep_iata = get_iata_code(departure)
    arr_iata = get_iata_code(destination)
    
    params = {
        "engine": "google_flights",
        "departure_id": dep_iata,
        "arrival_id": arr_iata,
        "outbound_date": date,
        "api_key": api_key,
        "currency": currency_code
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        flights = data.get("best_flights", [])[:3]
        if not flights:
            return ""
        
        result = f"[LIVE DATA] Available Flights from {departure} to {destination} on {date}:\n"
        for i, f in enumerate(flights, 1):
            flight_info = f.get('flights', [{}])[0]
            airline = flight_info.get('airline', 'Unknown')
            dep_time = flight_info.get('departure_airport', {}).get('time', 'N/A')
            arr_time = flight_info.get('arrival_airport', {}).get('time', 'N/A')
            price = f.get('price', 'N/A')
            result += f"{i}. {airline} - Departs {dep_time}, Arrives {arr_time} - Price: {currency_symbol}{price}\n"
        return result
    except Exception as e:
        print(f"[SYSTEM]: Error fetching flights: {str(e)}")
        return ""


def get_live_train_schedules(departure, destination, date, currency_symbol):
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    if not rapidapi_key:
        print("RAPIDAPI_KEY not found. Falling back to Google Maps Transit Scraper!")
        opts = get_live_google_transit(departure, destination, date, requested_mode="train", currency_symbol=currency_symbol)
        return "\n".join(opts) if opts else ""
        
    dep_code = get_station_code(departure)
    arr_code = get_station_code(destination)
    
    url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
    querystring = {"fromStationCode": dep_code, "toStationCode": arr_code, "dateOfJourney": date}
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        trains = data.get("data", [])[:3]
        if not trains:
            print("IRCTC returned no trains. Falling back to Google Maps Transit Scraper!")
            opts = get_live_google_transit(departure, destination, date, requested_mode="train", currency_symbol=currency_symbol)
            return "\n".join(opts) if opts else ""
            
        result = f"[LIVE DATA] Available Trains from {departure} to {destination} on {date}:\n"
        for i, t in enumerate(trains, 1):
            name = t.get('train_name', 'Unknown Train')
            number = t.get('train_number', '00000')
            dep_time = t.get('from_time', 'N/A')
            arr_time = t.get('to_time', 'N/A')
            
            mock_val = 30
            if "₹" in currency_symbol or "INR" in currency_symbol:
                mock_val = 2400
                
            result += f"{i}. {name} (Train {number}) - Departs {dep_time}, Arrives {arr_time} - Base Price: {currency_symbol}{mock_val}\n"
        return result
    except Exception as e:
        print(f"Error fetching rapidapi trains, firing fallback: {e}")
        opts = get_live_google_transit(departure, destination, date, requested_mode="train", currency_symbol=currency_symbol)
        return "\n".join(opts) if opts else ""

def availability_agent(state):
    print("--- Availability Agent Starting ---")
    
    dep = state.get("departure_city", "Unknown")
    dest = state.get("destination", "Unknown")
    date = state.get("start_date", "Unknown")
    mode = state.get("travel_mode", "Any").lower()
    
    currency_raw = state.get("currency", "USD ($)")
    currency_code = currency_raw.split(" ")[0]
    currency_symbol = currency_raw.split("(")[1].replace(")", "") if "(" in currency_raw else "$"
    
    print(f"Fetching live availability for {mode} from {dep} to {dest} on {date} in {currency_symbol}...")
    
    schedules = "Live Transit Schedules (DO NOT HALLUCINATE, ONLY USE THESE IF RELEVANT):\n"
    if mode in ["train", "any", "bus", "metro/cab"]:
        val = get_live_train_schedules(dep, dest, date, currency_symbol)
        if val: schedules += val + "\n"
    
    if mode in ["flight", "any"]:
        val = get_live_flight_schedules(dep, dest, date, currency_code, currency_symbol)
        if val: schedules += val + "\n"
        
    state["live_transit_schedules"] = schedules
    return state
