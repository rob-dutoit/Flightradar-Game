import json
import math
from fr24sdk.client import Client


def sandbox_fr24_api(airport_iata):

    radius_km = 100

    api_key = "019c89cf-ef0f-7271-9cf8-6f39f4b5c7cf|vYAT0ETgOLG5QQNv46J0l898OGs4IZOe2g3paEfpd1890fdf" #real #api_key = "019c7f8a-02a9-71b9-8aab-8e9f348a2872|nrwIwhNxSm0OX98p7aCdSOi1qkuPh4DXeOxerakZef18995a"

    # Load airport coordinates
    with open("airport_coords.json", "r") as f:
        airport_data = json.load(f)

    if airport_iata not in airport_data:
        raise ValueError(f"Airport {airport_iata} not found in airport_coords.json")

    lat, lon = airport_data[airport_iata]

    # Convert radius (km) to bounding box
    lat_delta = radius_km / 111
    lon_delta = radius_km / (111 * math.cos(math.radians(lat)))

    north = lat + lat_delta
    south = lat - lat_delta
    east = lon + lon_delta
    west = lon - lon_delta

    bounds = f"{north},{south},{west},{east}"

    # API call
    with Client(api_token=api_key) as client:
        result = client.live.flight_positions.get_full(
            bounds=bounds,
            gspeed="50-1000"
        )

    formatted_flights = []

    for aircraft in result.data:

        if aircraft.lat is None or aircraft.lon is None:
            continue

        formatted_flights.append({
            "flight_no": aircraft.callsign or aircraft.flight or "UNKNOWN",
            "lat": aircraft.lat,
            "long": aircraft.lon,
            "departure": aircraft.orig_iata or "UNK",
            "arrival": aircraft.dest_iata or "UNK",
            "track": aircraft.track or 0
        })

    with open("static/flights.json", "w") as f:
        json.dump(formatted_flights, f, indent=4)

    return len(formatted_flights)