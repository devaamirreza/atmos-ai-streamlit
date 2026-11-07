import requests


def get_weather(city):
    """
    Fetch current weather information for a given city.
    """

    try:
        # STEP 1: Convert city name into geographical coordinates

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=15
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        # STEP 2: Check whether the city exists

        if not geo_data.get("results"):
            return {
                "error": f"City '{city}' not found."
            }

        # STEP 3: Extract location information

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "Unknown")

        # STEP 4: Retrieve weather information

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
                "cloud_cover"
            ],
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=15
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current"]

        # STEP 5: Return structured weather information

        return {
            "city": city_name,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "temperature_celsius": current["temperature_2m"],
            "feels_like_celsius": current["apparent_temperature"],
            "humidity_percent": current["relative_humidity_2m"],
            "precipitation_mm": current["precipitation"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "cloud_cover_percent": current["cloud_cover"],
            "weather_code": current["weather_code"],
            "observation_time": current["time"]
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Weather service timed out. Please try again."
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": "Unable to connect to the weather service. Check your internet connection."
        }

    except requests.exceptions.HTTPError as error:
        return {
            "error": f"Weather API returned an HTTP error: {error}"
        }

    except (ValueError, KeyError, IndexError) as error:
        return {
            "error": f"Unable to process weather data: {error}"
        }

    except requests.exceptions.RequestException as error:
        return {
            "error": f"Weather request failed: {error}"
        }