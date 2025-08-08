import tkinter as tk
import requests
import threading

def fetch_weather(city):
    try:
        # Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if "results" not in geo_data:
            result_label.config(text="City not found.")
            return

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        location_name = geo_data["results"][0]["name"]

        # Get weather data
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m"
        )
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        temperature = weather_data["current"]["temperature_2m"]

        result_label.config(
            text=f"Weather in {location_name}:\nTemperature: {temperature} °C"
        )

    except Exception as e:
        result_label.config(text="Error fetching weather.")

def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return
    result_label.config(text="Loading...")
    # Run fetch_weather in a separate thread
    threading.Thread(target=fetch_weather, args=(city,), daemon=True).start()

# Tkinter UI
root = tk.Tk()
root.title("Weather App (Open-Meteo)")
root.geometry("300x200")

tk.Label(root, text="Enter City Name:").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack()

tk.Button(root, text="Get Weather", command=get_weather).pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
