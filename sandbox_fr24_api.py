import json
import math
from fr24sdk.client import Client

def getAircraftAroundAirport(airport_iata, radius_km, api_key):
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
        result = client.live.flight_positions.get_full(bounds=bounds)

    return result

airport_iata = "TSV"
radius_km = 100
#api_key = "019c89cf-ef0f-7271-9cf8-6f39f4b5c7cf|vYAT0ETgOLG5QQNv46J0l898OGs4IZOe2g3paEfpd1890fdf" #real
api_key = "019c7f8a-02a9-71b9-8aab-8e9f348a2872|nrwIwhNxSm0OX98p7aCdSOi1qkuPh4DXeOxerakZef18995a" #sandbox

flights = getAircraftAroundAirport(airport_iata, radius_km, api_key)

#print(type(flights))          # Response object
#print(flights.data)    # List
print(flights.data[0])  # Individual aircraft