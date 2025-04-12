import datetime
import requests
import psutil
import platform
import tkinter as tk
from tkinter import scrolledtext
from suntime import Sun
from dateutil import tz

def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        ip = data.get('ip', 'Unknown')
        isp = data.get('org', 'Unknown')
        loc = data.get('loc', '0,0').split(',')
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        latitude = float(loc[0]) if loc[0] else 0.0
        longitude = float(loc[1]) if loc[1] else 0.0
        return ip, isp, latitude, longitude, city, region, country
    except Exception as e:
        return 'Unknown', 'Unknown', 0.0, 0.0, 'Unknown', 'Unknown', 'Unknown'

def get_continent(country_code):
    # Simple mapping of country codes to continents
    continent_map = {
        'US': 'North America', 'CA': 'North America', 'MX': 'North America',
        'GB': 'Europe', 'FR': 'Europe', 'DE': 'Europe', 'IT': 'Europe', 'ES': 'Europe',
        'CN': 'Asia', 'JP': 'Asia', 'IN': 'Asia', 'KR': 'Asia',
        'AU': 'Oceania', 'NZ': 'Oceania',
        'BR': 'South America', 'AR': 'South America', 'CL': 'South America',
        'ZA': 'Africa', 'NG': 'Africa', 'EG': 'Africa',
    }
    return continent_map.get(country_code, 'Unknown')

def get_sun_times(latitude, longitude):
    try:
        sun = Sun(latitude, longitude)
        today = datetime.date.today()
        sunrise = sun.get_sunrise_time()
        sunset = sun.get_sunset_time()
        local_tz = tz.tzlocal()
        sunrise = sunrise.astimezone(local_tz)
        sunset = sunset.astimezone(local_tz)
        return sunrise, sunset
    except Exception:
        return None, None

def get_system_info():
    try:
        processor = platform.processor() or 'Unknown'
        system = platform.node() or 'Unknown Device'
        memory = psutil.virtual_memory()
        total_memory = memory.total / (1024 ** 3)  # Convert to GB
        return processor, system, total_memory
    except Exception:
        return 'Unknown', 'Unknown Device', 0.0

def create_gui():
    # Fetch all data
    today = datetime.date.today()
    date_str = today.strftime("%d.%m.%Y")
    ip, isp, latitude, longitude, city, region, country = get_ip_info()
    sunrise, sunset = get_sun_times(latitude, longitude)
    sunrise_str = sunrise.strftime("%H:%M") if sunrise else "Unknown"
    sunset_str = sunset.strftime("%H:%M") if sunset else "Unknown"
    processor, system, total_memory = get_system_info()
    continent = get_continent(country)

    # Location description
    if city != 'Unknown' and country != 'Unknown':
        county = region if region != 'Unknown' else 'Unknown County'
        location_desc = (f"This is {city} situated in the county of {county}, "
                        f"in the country of {country}, which is in {continent}.")
    else:
        location_desc = "Location details unavailable."

    # Create GUI
    root = tk.Tk()
    root.title("System and Location Summary")
    root.geometry("600x500")
    # Center the window
    root.eval('tk::PlaceWindow . center')

    # Create scrolled text area
    text_area = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, width=70, height=25, font=("Arial", 12)
    )
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Helper function to insert formatted text
    def insert_text(label, value, is_heading=False):
        text_area.insert(tk.END, label, "bold" if is_heading else "normal")
        if not is_heading:
            text_area.insert(tk.END, f"{value}\n")
        else:
            text_area.insert(tk.END, "\n")

    # Configure tags for formatting
    text_area.tag_configure("bold", font=("Arial", 12, "bold"))
    text_area.tag_configure("normal", font=("Arial", 12))

    # Insert data into text area
    insert_text("System and Location Summary", "", is_heading=True)
    insert_text("Today is: ", date_str)
    insert_text("Sunrise is/was at: ", sunrise_str)
    insert_text("Sunset is/was at: ", sunset_str)
    insert_text("IP Address: ", ip)
    insert_text("ISP: ", isp)
    insert_text("Device: ", system)
    insert_text("Processor: ", processor)
    insert_text("Total Memory: ", f"{total_memory:.2f} GB")
    insert_text("Location: ", city)
    insert_text("GPS Coordinates: ", f"Latitude: {latitude:.6f}, Longitude: {longitude:.6f}")
    insert_text("Location Description: ", location_desc)

    # Make text area read-only
    text_area.config(state='disabled')

    # Run the GUI
    root.mainloop()

def main():
    create_gui()

if __name__ == "__main__":
    main()
