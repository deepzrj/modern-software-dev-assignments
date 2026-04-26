import requests
import sys
import logging
from .config import OPENWEATHER_API_KEY, BASE_URL

# Configure logging to stderr so it doesn't interfere with STDIO transport
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("weather-server")

def get_current_weather(city: str) -> dict:
    if not OPENWEATHER_API_KEY:
        logger.error("Missing OpenWeather API Key")
        return {"error": "API key not configured on server"}

    url = f"{BASE_URL}/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    try:
        logger.info(f"Fetching current weather for {city}")
        response = requests.get(url, params=params, timeout=10)
        
        # Handle Rate Limiting (Requirement 3)
        if response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again in a minute."}
            
        if response.status_code != 200:
            return {"error": f"OpenWeather API error: {response.status_code}"}

        data = response.json()
        return {
            "city": data.get("name", city),
            "temperature": f"{data['main']['temp']}°C",
            "condition": data["weather"][0]["description"],
            "humidity": f"{data['main']['humidity']}%"
        }

    except requests.exceptions.Timeout:
        return {"error": "The weather service timed out."}
    except Exception as e:
        logger.exception("Unexpected error in get_current_weather")
        return {"error": str(e)}

def get_weather_forecast(city: str) -> dict:
    if not OPENWEATHER_API_KEY:
        logger.error("Missing OpenWeather API Key")
        return {"error": "API key not configured on server"}

    url = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "cnt": 5}

    try:
        logger.info(f"Fetching weather forecast for {city}")
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again in a minute."}

        if response.status_code != 200:
            return {"error": f"OpenWeather API error: {response.status_code}"}

        data = response.json()
        forecast = []
        for entry in data.get("list", []):
            forecast.append(
                {
                    "time": entry.get("dt_txt"),
                    "temperature": f"{entry['main']['temp']}°C",
                    "condition": entry["weather"][0]["description"],
                    "humidity": f"{entry['main']['humidity']}%",
                }
            )

        if not forecast:
            return {"error": "No forecast data returned for this city"}

        return {
            "city": data.get("city", {}).get("name", city),
            "forecast": forecast,
        }

    except requests.exceptions.Timeout:
        return {"error": "The weather service timed out."}
    except Exception as e:
        logger.exception("Unexpected error in get_weather_forecast")
        return {"error": str(e)}
