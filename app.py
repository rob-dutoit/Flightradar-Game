from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)

def geocode_city(city):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "flask-leaflet-app"}
    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    if not data:
        return None

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"])
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/geocode")
def geocode():
    city = request.args.get("city")
    result = geocode_city(city)
    return jsonify(result or {})

if __name__ == "__main__":
    app.run(debug=True)