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
    """Fetch 7-day forecast with extended metrics."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weather_code",
            "sunrise",
            "sunset",
            "uv_index_max",
            "precipitation_probability_max",
            "wind_speed_10m_max"
        ],
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
    if code == 0: return "☀️"
    if 1 <= code <= 3: return "⛅"
    if 45 <= code <= 48: return "🌫️"
    if 51 <= code <= 67: return "🌧️"
    if 71 <= code <= 77: return "❄️"
    if 80 <= code <= 82: return "🌦️"
    if 95 <= code <= 99: return "⛈️"
    return "🌡️"

def generate_html(city, data):
    """Generate rich HTML report."""
    daily = data["daily"]
    dates = daily["time"]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    precip_sum = daily["precipitation_sum"]
    precip_prob = daily["precipitation_probability_max"]
    codes = daily["weather_code"]
    sunrise = daily["sunrise"]
    sunset = daily["sunset"]
    uv_index = daily["uv_index_max"]
    wind = daily["wind_speed_10m_max"]
    
    cards = ""
    for i in range(len(dates)):
        date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
        full_date = date_obj.strftime("%d %B")
        emoji = get_weather_emoji(codes[i])
        
        # Format times
        sr = datetime.fromisoformat(sunrise[i]).strftime("%H:%M")
        ss = datetime.fromisoformat(sunset[i]).strftime("%H:%M")
        
        cards += f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="day-name">{day_name}</div>
                    <div class="date">{full_date}</div>
                </div>
                <div class="weather-icon">{emoji}</div>
            </div>
            <div class="temps">
                <span class="max">{max_temps[i]}°</span>
                <span class="min">{min_temps[i]}°</span>
            </div>
            <div class="details">
                <div class="detail-item"><span>☔ Rain</span> <span>{precip_prob[i]}% ({precip_sum[i]}mm)</span></div>
                <div class="detail-item"><span>💨 Wind</span> <span>{wind[i]} km/h</span></div>
                <div class="detail-item"><span>☀️ UV</span> <span>{uv_index[i]}</span></div>
                <div class="detail-item"><span>🌅 Sun</span> <span>{sr} - {ss}</span></div>
            </div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Forecast - {city}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
            
            body {{ 
                font-family: 'Outfit', sans-serif; 
                background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
                margin: 0; 
                padding: 40px 20px; 
                color: #2c3e50; 
                min-height: 100vh;
            }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ 
                text-align: center; 
                color: white; 
                font-size: 2.5em; 
                margin-bottom: 40px; 
                text-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            }}
            .grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
                gap: 20px; 
            }}
            .card {{ 
                background: rgba(255, 255, 255, 0.95); 
                border-radius: 20px; 
                padding: 25px; 
                box-shadow: 0 10px 20px rgba(0,0,0,0.1); 
                transition: transform 0.3s; 
            }}
            .card:hover {{ transform: translateY(-5px); }}
            .card-header {{ 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 15px; 
            }}
            .day-name {{ font-weight: 600; font-size: 1.2em; }}
            .date {{ font-size: 0.9em; color: #7f8c8d; }}
            .weather-icon {{ font-size: 2.5em; }}
            .temps {{ 
                font-size: 2.5em; 
                font-weight: 300; 
                margin: 15px 0; 
                display: flex; 
                gap: 15px; 
                align-items: baseline; 
            }}
            .min {{ font-size: 0.6em; color: #95a5a6; }}
            .details {{ margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px; }}
            .detail-item {{ 
                display: flex; 
                justify-content: space-between; 
                margin-bottom: 8px; 
                font-size: 0.9em; 
            }}
            .footer {{ 
                text-align: center; 
                margin-top: 50px; 
                color: rgba(255,255,255,0.8); 
                font-size: 0.9em; 
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌤️ 7-Day Forecast: {city}</h1>
            <div class="grid">
                {cards}
            </div>
            <div class="footer">
                Powered by Open-Meteo API • Generated by Python Toolbox
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
    
    logging.info("🌤️  Fetching extended 7-day forecast...")
    data = get_forecast(lat, lon)
    
    if not data:
        sys.exit(1)
        
    # Console Output
    print("\n-------------------------------------------------------------------------")
    print(f" 📅 7-Day Forecast for {found_name}")
    print("-------------------------------------------------------------------------")
    print(f"{'Date':<12} | {'Wx':<3} | {'Min/Max':<9} | {'Rain':<9} | {'Wind':<8} | {'UV':<3}")
    print("-------------------------------------------------------------------------")
    
    daily = data["daily"]
    for i in range(len(daily["time"])):
        date_obj = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        date = date_obj.strftime("%a %d")
        min_t = round(daily["temperature_2m_min"][i])
        max_t = round(daily["temperature_2m_max"][i])
        rain_sum = daily["precipitation_sum"][i]
        rain_prob = daily["precipitation_probability_max"][i]
        wind = round(daily["wind_speed_10m_max"][i])
        uv = round(daily["uv_index_max"][i])
        code = daily["weather_code"][i]
        emoji = get_weather_emoji(code)
        
        temp_str = f"{min_t}/{max_t}°"
        rain_str = f"{rain_prob}%" if rain_prob > 0 else "0%"
        if rain_sum > 0:
             rain_str += f" ({rain_sum}mm)"
             
        print(f"{date:<12} | {emoji:<3} | {temp_str:<9} | {rain_str:<9} | {wind}km/h   | {uv:<3}")
        
    print("-------------------------------------------------------------------------\n")
    
    # HTML Output
    logging.info("📄 Generating rich HTML report...")
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
