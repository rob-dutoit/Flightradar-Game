import pandas as pd
import requests
from bs4 import BeautifulSoup

# ----------------------------
# 1. Fetch Wikipedia page
# ----------------------------
wiki_url = "https://en.wikipedia.org/wiki/List_of_busiest_airports_by_passenger_traffic"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}

response = requests.get(wiki_url, headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to fetch page: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# ----------------------------
# 2. Find the first table
# ----------------------------
table = soup.find("table", {"class": "wikitable"})

# ----------------------------
# 3. Parse table rows
# ----------------------------
rows = table.find_all("tr")
data = []

for row in rows[1:]:  # skip header
    cols = row.find_all(["td", "th"])
    cols = [c.get_text(strip=True) for c in cols]
    if len(cols) >= 4:  # ensure enough columns
        rank = cols[0]
        airport = cols[1]
        iata = cols[2]
        passengers = cols[3].replace(",", "")
        data.append([rank, airport, iata, passengers])

traffic_df = pd.DataFrame(data, columns=["Rank", "Airport", "IATA", "Passengers (2023)"])

# Only top 250
traffic_df = traffic_df.head(250)

# ----------------------------
# 4. Load Flightradar CSV
# ----------------------------
fr_df = pd.read_csv("flightradar24_airports.csv")

fr_df = fr_df.rename(columns={
    "iata": "IATA",
    "icao": "ICAO",
    "country": "Country",
    "lat": "Latitude",
    "lon": "Longitude"
})

# ----------------------------
# 5. Merge by IATA
# ----------------------------
merged = pd.merge(
    traffic_df,
    fr_df[["IATA", "ICAO", "Country", "Latitude", "Longitude"]],
    on="IATA",
    how="left"
)

# ----------------------------
# 6. Save CSV
# ----------------------------
merged.to_csv("top250_busiest_airports.csv", index=False)

print("✅ Done! Saved top250_busiest_airports.csv")
print(merged.head())