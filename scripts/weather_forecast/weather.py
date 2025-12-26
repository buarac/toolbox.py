#!/usr/bin/env python3
"""
Weather Forecast Tool 🌤️

Fetches 7-day weather forecast for a specified city using Open-Meteo API.
Displays a summary in the console and opens a detailed HTML report in the browser.

Arguments:
    --city: Name of the city (default: Paris)

Example:
    python3 scripts/weather_forecast/weather.py --city "New York"
"""
import argparse
import logging
import sys
import webbrowser
import tempfile
from pathlib import Path
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def setup_args():
    parser = argparse.ArgumentParser(description="Weather Forecast Tool")
    parser.add_argument("--city", type=str, default="Paris", help="City name (default: Paris)")
    return parser.parse_args()

def get_coordinates(city_name):
    """Fetch latitude and longitude for a city."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            return None, None, None
            
        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"]
    except requests.RequestException as e:
        logging.error(f"❌ Connection error (Geocoding): {e}")
        return None, None, None

def get_forecast(lat, lon):
    """Fetch 7-day forecast."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "weather_code"],
        "timezone": "auto"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"❌ Connection error (Forecast): {e}")
        return None

def get_weather_emoji(code):
    """Map WMO weather code to emoji."""
    # Simplified mapping
    if code == 0: return "☀️"
    if 1 <= code <= 3: return "⛅"
    if 45 <= code <= 48: return "🌫️"
    if 51 <= code <= 67: return "🌧️"
    if 71 <= code <= 77: return "❄️"
    if 80 <= code <= 82: return "🌦️"
    if 95 <= code <= 99: return "⛈️"
    return "🌡️"

def generate_html(city, data):
    """Generate HTML report."""
    daily = data["daily"]
    dates = daily["time"]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    precip = daily["precipitation_sum"]
    codes = daily["weather_code"]
    
    rows = ""
    for i in range(len(dates)):
        date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
        date_str = date_obj.strftime("%A %d %b")
        emoji = get_weather_emoji(codes[i])
        
        rows += f"""
        <tr>
            <td>{date_str}</td>
            <td style="font-size: 1.5em;">{emoji}</td>
            <td class="temp-min">{min_temps[i]}°C</td>
            <td class="temp-max">{max_temps[i]}°C</td>
            <td>{precip[i]} mm</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Forecast - {city}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ text-align: center; color: #1a73e8; margin-bottom: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 15px; text-align: center; border-bottom: 1px solid #eee; }}
            th {{ background-color: #f8f9fa; color: #5f6368; font-weight: 600; }}
            tr:hover {{ background-color: #f8f9fa; }}
            .temp-max {{ color: #d93025; font-weight: bold; }}
            .temp-min {{ color: #1a73e8; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 0.9em; color: #666; }}
            a {{ color: #1a73e8; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌤️ Weather Forecast: {city}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Weather</th>
                        <th>Min Temp</th>
                        <th>Max Temp</th>
                        <th>Precipitation</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <div class="footer">
                Genereted by Python Toolbox via Open-Meteo API
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def main():
    args = setup_args()
    city = args.city
    
    logging.info(f"🌍 Searching for city: {city}...")
    lat, lon, found_name = get_coordinates(city)
    
    if not lat:
        logging.error(f"❌ City '{city}' not found.")
        sys.exit(1)
        
    logging.info(f"📍 Found: {found_name} ({lat:.2f}, {lon:.2f})")
    
    logging.info("🌤️  Fetching 7-day forecast...")
    data = get_forecast(lat, lon)
    
    if not data:
        sys.exit(1)
        
    # Console Output
    print("\n------------------------------------------------")
    print(f" 📅 7-Day Forecast for {found_name}")
    print("------------------------------------------------")
    print(f"{'Date':<15} | {'Cond':<4} | {'Min':<6} | {'Max':<6} | {'Rain':<6}")
    print("------------------------------------------------")
    
    daily = data["daily"]
    for i in range(len(daily["time"])):
        date = daily["time"][i]
        min_t = daily["temperature_2m_min"][i]
        max_t = daily["temperature_2m_max"][i]
        rain = daily["precipitation_sum"][i]
        code = daily["weather_code"][i]
        emoji = get_weather_emoji(code)
        
        print(f"{date:<15} | {emoji:<4} | {min_t:>4} °C | {max_t:>4} °C | {rain:>4} mm")
    print("------------------------------------------------\n")
    
    # HTML Output
    logging.info("📄 Generating HTML report...")
    html_content = generate_html(found_name, data)
    
    try:
        # Create a temporary file
        fd, path = tempfile.mkstemp(suffix=".html", prefix=f"weather_{found_name}_")
        with os.fdopen(fd, 'w') as f:
            f.write(html_content)
            
        logging.info(f"🚀 Opening report in browser: {path}")
        webbrowser.open(f"file://{path}")
        
    except Exception as e:
        logging.error(f"❌ Failed to open browser: {e}")

if __name__ == "__main__":
    import os # Late import for os.fdopen used in main
    main()
