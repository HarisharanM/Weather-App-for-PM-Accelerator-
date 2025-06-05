import streamlit as st
import requests
from datetime import datetime
from database import session, WeatherEntry  
import pandas as pd

def detect_location_by_ip():
    try:
        ip_info = requests.get("https://ipinfo.io").json()
        city = ip_info.get("city")
        return city
    except:
        return None

API_KEY = "5547ff3f731b612bac12efbce295444c"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "City": data["name"],
            "Temperature (°C)": data["main"]["temp"],
            "Condition": data["weather"][0]["description"].title(),
            "Humidity (%)": data["main"]["humidity"],
            "Wind (m/s)": data["wind"]["speed"]
        }
        return weather
    else:
        return None

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecasts = []
        for item in data["list"]:
            dt_txt = item["dt_txt"]
            if "12:00:00" in dt_txt:
                forecast = {
                    "Date": dt_txt.split(" ")[0],
                    "Temp (°C)": item["main"]["temp"],
                    "Condition": item["weather"][0]["description"].title()
                }
                forecasts.append(forecast)
        return forecasts
    else:
        return None

st.title("🌤 Simple Weather App")

city = st.text_input("Enter city name")

if st.button("📍 Auto-Detect My Location"):
    detected_city = detect_location_by_ip()
    if detected_city:
        st.success(f"Detected location: {detected_city}")
        city = detected_city
    else:
        st.error("Could not detect location.")

if city:
    weather = get_weather(city)
    if weather:
        st.subheader("Current Weather:")
        for key, value in weather.items():
            st.write(f"**{key}:** {value}")

                
        existing_entry = session.query(WeatherEntry).filter_by(
            city=weather["City"],
            date=str(datetime.today().date())
        ).first()

        if not existing_entry:
            new_entry = WeatherEntry(
                city=weather["City"],
                date=str(datetime.today().date()),
                temperature=weather["Temperature (°C)"],
                condition=weather["Condition"]
            )
            session.add(new_entry)
            session.commit()
            st.success("✅ Auto-saved today's weather to history!")
        else:
            st.info("✅ Weather for today already saved.")

    st.subheader("🌦 5-Day Forecast:")
    forecast = get_forecast(city)
    if forecast:
        for day in forecast:
            st.write(f"📅 {day['Date']} - 🌡 {day['Temp (°C)']}°C - {day['Condition']}")
    else:
        st.warning("Could not load forecast data.")

st.subheader("📜 Saved Weather History")
entries = session.query(WeatherEntry).all()

if entries:
    for entry in entries:
        st.write(f"📍 {entry.city} | 📅 {entry.date} | 🌡 {entry.temperature}°C | 🌥 {entry.condition}")
else:
    st.info("No weather history saved yet.")
