import requests
import pandas as pd

url = "https://www.flightradar24.com/_json/airports.php"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed:", response.status_code)
    exit()

data = response.json()

airports = []

for airport in data["rows"]:
    airports.append({
        "name": airport.get("name"),
        "iata": airport.get("iata"),
        "icao": airport.get("icao"),
        "country": airport.get("country"),
        "lat": airport.get("lat"),
        "lon": airport.get("lon")
    })

df = pd.DataFrame(airports)
df.to_csv("flightradar24_airports.csv", index=False)

print(f"Saved {len(df)} airports")
print(df.head())