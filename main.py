import json
import requests
from tkinter import *
from tkinter import messagebox
import sys
from requests import HTTPError

SERVICE_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
LOCATION_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
BACKGROUND = "black"
API_KEY = "a8a33ec79eaa1b91cc0678875cb2b1c7"
global lat, lon, location_response, weather_icon


# LOCATION = "Doha"


# FUNCTIONALITY
def search_city():
    get_location(city_entry.get())


# API CONNECTION
def get_location(city_name: str):
    global lat, lon, location_response
    location_parameters = {
        'q': city_name.capitalize(),
        'limit': 1,
        'appid': API_KEY
    }
    try:
        location_response = requests.get(LOCATION_ENDPOINT, params=location_parameters)
        # print(location_response.json())
        location_response.raise_for_status()
        lat = location_response.json()[0]['lat']
        lon = location_response.json()[0]['lon']
        city_entry.destroy()
        city_label.destroy()
        search_button.destroy()
        show_weather()
    except IndexError:
        messagebox.showerror(title="City Search", message="No city found!")
    except HTTPError:
        messagebox.showerror(title="City Search", message="Failed connection to the server!")


def weather_data():
    weather_parameters = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    weather_response = requests.get(SERVICE_ENDPOINT, params=weather_parameters)
    # print(weather_response.json())
    return weather_response.json()


# # UI
window = Tk()
window.config(padx=50, pady=50, background=BACKGROUND)
window.title("The Weather App v1.0")
# INITIAL UI
city_label = Label(text="Please Enter a City:", padx=25, pady=25, background=BACKGROUND, foreground="white",
                   font=("Ariel", 20, "bold"))
city_label.grid(column=0, row=0)

city_entry = Entry(font=("Ariel", 20, "bold"), width=20)
city_entry.focus()
city_entry.grid(row=1, column=0)

search_icon_file = PhotoImage(file="search_icon.png")
search_button = Button(image=search_icon_file, command=search_city)
search_button.config(highlightthickness=0, background=BACKGROUND, pady=25, padx=25, height=50, width=50)
search_button.grid(row=3, column=0)


def show_weather():
    global weather_icon
    data = weather_data()
    temp = data['main']['temp']
    feels_like_temp = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    if "d" in data['weather'][0]['icon']:
        BACKGROUND = "#FFC300"
        weather_icon_retrieved = str(data['weather'][0]['icon']) + '.png'
        weather_icon = PhotoImage(file=f"./images/{weather_icon_retrieved}")
        window.config(background=BACKGROUND)
    else:
        BACKGROUND = "#2E2D2A"
        weather_icon_retrieved = str(data['weather'][0]['icon']) + '.png'
        weather_icon = PhotoImage(file=f"./images/{weather_icon_retrieved}")
        day = False
        window.config(background=BACKGROUND)
        # print("night time")
    # print(temp, feels_like_temp, humidity, wind_speed, day)
    # window.config(background=BACKGROUND)
    canvas = Canvas(width=100, height=100, bg=BACKGROUND, highlightthickness=0)
    canvas.create_image(50, 50, image=weather_icon)
    canvas.grid(row=2, column=0)

    temp_label = Label(text=f"Current Temperature: {temp}°C", font=("Ariel", 12, "bold"), foreground="white",
                       background=BACKGROUND)
    temp_label.grid(row=3, column=0)

    feels_temp_label = Label(text=f"It Feels Like: {feels_like_temp}°C", font=("Ariel", 12, "bold"),
                             foreground="white", background=BACKGROUND)
    feels_temp_label.grid(row=4, column=0)

    humidity_label = Label(text=f"Humidity: {humidity}%", font=("Ariel", 12, "bold"),
                           foreground="white", background=BACKGROUND)
    humidity_label.grid(row=5, column=0)

    wind_label = Label(text=f"Wind Speed: {wind_speed}km/h", font=("Ariel", 12, "bold"),
                       foreground="white", background=BACKGROUND)
    wind_label.grid(row=6, column=0)

    country_label = Label(text=f"{data['name']}, {data['sys']['country']}", font=("Ariel", 12, "bold"),
                          foreground="white", background=BACKGROUND)
    country_label.grid(row=0, column=0)

    weather_description = str(data['weather'][0]['description']).capitalize()
    weather_description_label = Label(text=f"{weather_description}", font=("Ariel", 12, "bold"),
                                      foreground="white", background=BACKGROUND)
    weather_description_label.grid(row=1, column=0)


window.mainloop()
