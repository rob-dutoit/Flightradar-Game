import csv
import json

# Read CSV and convert to JSON
with open('flights_test.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

with open('flights_test.json', 'w') as jsonfile:
    json.dump(data, jsonfile, indent=4)