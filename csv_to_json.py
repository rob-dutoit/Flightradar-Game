import csv
import json

input_file = "flightradar24_airports.csv"
output_file = "airport_coords.json"

airport_coords = {}

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        iata = row["iata"]
        lat = float(row["lat"])
        lon = float(row["lon"])
        airport_coords[iata] = [lat, lon]

with open(output_file, "w", encoding="utf-8") as jsonfile:
    json.dump(airport_coords, jsonfile, indent=2)

print("Done. Created airport_coords.json")