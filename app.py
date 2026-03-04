from flask import Flask, render_template, request, jsonify
import requests
import json
from sandbox_fr24_api import sandbox_fr24_api  # Make sure this exists and generates flights.json

app = Flask(__name__)

# --- Helper: geocode city names ---
def geocode_city(city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    headers = {"User-Agent": "flask-leaflet-app"}
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    if not data:
        return None
    return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}

# --- Main page ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Geocode endpoint ---
@app.route("/geocode")
def geocode():
    city = request.args.get("city")
    result = geocode_city(city)
    return jsonify(result or {})

# --- Start a new game: generate flights for current departure airport ---
@app.route("/start_game")
def start_game():
    # Load the game.json to get the departure airport
    with open("static/game.json", "r") as f:
        game_data = json.load(f)

    departure_airport = game_data["departure"]

    # Call your API to generate flights.json
    sandbox_fr24_api(departure_airport)

    # Load the newly generated flights.json
    with open("static/flights.json", "r") as f:
        flights = json.load(f)

    # Return the flights to the frontend
    return jsonify({"status": "success", "flights": flights})

# --- Update flights for a different airport manually ---
@app.route("/update_flights/<airport_code>")
@app.route("/update_flights/<airport_code>")
def update_flights(airport_code):
    # Generate flights.json for the new airport
    sandbox_fr24_api(airport_code)

    # Load the new flights
    with open("static/flights.json", "r") as f:
        flights = json.load(f)

    return jsonify({"status": "success", "flights": flights})
if __name__ == "__main__":
    app.run(debug=True)