import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    if not WEATHER_API_KEY:
        print("Warning: WEATHER_API_KEY not found in environment variables.")
        return {"temperature": "N/A", "description": "Weather data unavailable (No API Key)"}

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather = {
            "temperature": data.get("main", {}).get("temp", "N/A"),
            "description": data.get("weather", [{}])[0].get("description", "No description")
        }

        return weather
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {"temperature": "N/A", "description": f"Weather data unavailable ({str(e)})"}