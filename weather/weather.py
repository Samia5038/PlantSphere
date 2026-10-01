import requests


WEATHER_LABELS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with hail",
}


def get_weather_data(city):
    try:
        location_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        location_response.raise_for_status()
        locations = location_response.json().get("results", [])
        if not locations:
            return {"error": "No matching location found. Try another city name."}

        location = locations[0]
        forecast_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,apparent_temperature,"
                    "precipitation,weather_code,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        forecast_response.raise_for_status()
        current = forecast_response.json().get("current", {})
        code = current.get("weather_code")
        return {
            "city": location.get("name", city),
            "country": location.get("country", ""),
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "precipitation": current.get("precipitation"),
            "wind_speed": current.get("wind_speed_10m"),
            "condition": WEATHER_LABELS.get(code, "Current conditions"),
            "updated_at": current.get("time"),
        }
    except requests.RequestException:
        return {"error": "Weather service is unavailable. Check your internet connection."}
    except (KeyError, TypeError, ValueError):
        return {"error": "Weather data could not be read for that location."}