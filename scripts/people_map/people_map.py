#!/usr/bin/env python3
"""
People Map Tool 🌍

A Flask web application to visualize people on a map.
- Inputs: Name, City via Web Interface
- Processing: Auto-detects Country and Coordinates (Open-Meteo Geocoding)
- Output: Interactive Map (LeafletJS)

Usage:
    python3 scripts/people_map/people_map.py
"""
import json
import logging
import os
import threading
import webbrowser
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

# Helper to find resources relative to this script
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "people.json"
TEMPLATE_DIR = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Persistence ---


def load_data():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return []


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Failed to save data: {e}")


# --- Geocoding ---


def geocode_city(city_name):
    """Fetch lat, lon, and country from Open-Meteo."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return None

        result = data["results"][0]
        return {
            "lat": result["latitude"],
            "lon": result["longitude"],
            "country": result.get("country", "Unknown"),
            "city_name": result["name"],  # Normalized name
        }
    except Exception as e:
        logging.error(f"Geocoding error: {e}")
        return None


# --- Routes ---


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/people", methods=["GET"])
def get_people():
    people = load_data()
    return jsonify(people)


@app.route("/api/add", methods=["POST"])
def add_person():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    city = data.get("city")

    if not all([first_name, last_name, city]):
        return jsonify({"error": "Missing fields"}), 400

    # Geocode
    geo = geocode_city(city)
    if not geo:
        return jsonify({"error": "City not found"}), 404

    new_person = {
        "id": os.urandom(4).hex(),
        "first_name": first_name,
        "last_name": last_name,
        "city": geo["city_name"],
        "country": geo["country"],
        "lat": geo["lat"],
        "lon": geo["lon"],
    }

    people = load_data()
    people.append(new_person)
    save_data(people)

    return jsonify(new_person)


@app.route("/api/delete/<person_id>", methods=["DELETE"])
def delete_person(person_id):
    people = load_data()
    people = [p for p in people if p["id"] != person_id]
    save_data(people)
    return jsonify({"success": True})


# --- Main ---


def open_browser():
    """Open browser after a short delay."""
    webbrowser.open("http://127.0.0.1:5000")


def main():
    # Check dependencies check is done by toolbox mostly,
    # but good to be standalone executable too.

    logging.info("🚀 Starting People Map Server...")
    logging.info("🌍 Open http://127.0.0.1:5000 in your browser")

    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true" and not os.environ.get("NO_BROWSER"):
        # Only open browser on the primary process, not the reloader
        threading.Timer(1.5, open_browser).start()

    port = int(os.environ.get("PORT", 5001))
    app.run(host="127.0.0.1", port=port, debug=debug_mode)


if __name__ == "__main__":
    main()
