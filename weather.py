import customtkinter as ctk
import requests
import geocoder
import secrets


class WeatherDisplayFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the WeatherDisplayFrame.

        Parameters:
        - parent: The parent widget or window where this frame will be placed.
        - *args, **kwargs: Additional arguments and keyword arguments.

        This constructor fetches weather data and creates weather display elements.
        """
        super().__init__(parent, *args, **kwargs)
        self.API_KEY = secrets.API_KEY
        self.BASE_URL = "http://api.weatherapi.com/v1/"

        # Get user's geolocation
        geocode = geocoder.ip('me')
        if geocode.ok:
            location_lat, location_long = geocode.latlng
        else:
            print("Unable to retrieve current location.")

        # Build the request URL for current weather data
        request_url = self.BASE_URL + "current.json?" + "key=" + self.API_KEY + "&q=" + str(location_lat) + "," + str(
            location_long)
        response = requests.get(request_url).json()
        location_name = response['location']['name']

        # Fetch daily weather data
        daily_response = requests.get(
            f'http://api.weatherapi.com/v1/forecast.json?key={self.API_KEY}&q={location_name}&days=7').json()
        data = daily_response['forecast']['forecastday']

        # Extract current weather information
        current_temp = response['current']['temp_f']
        current_condition = response['current']['condition']['text']
        maxTemp = daily_response['forecast']['forecastday'][0]['day']['maxtemp_f']
        minTemp = daily_response['forecast']['forecastday'][0]['day']['mintemp_f']

        # Create and place the weather display elements within the frame
        self.create_weather_elements(current_temp, current_condition, maxTemp, minTemp)

    def create_weather_elements(self, current_temp, current_condition, maxTemp, minTemp):
        """
        Create and place weather display elements within the frame.

        Parameters:
        - current_temp: Current temperature in Fahrenheit.
        - current_condition: Current weather condition.
        - maxTemp: Maximum temperature of the day in Fahrenheit.
        - minTemp: Minimum temperature of the day in Fahrenheit.

        This function creates and positions labels for weather description, temperature, and max/min temperatures.
        """
        # Description label
        description_label = ctk.CTkLabel(self, text=str(current_condition).title(), font=("Times", 24, "italic"),
                                         text_color="#000000")
        description_label.place(relx=0.5, rely=0.2, anchor='center')

        # Temperature label
        temperature = ctk.CTkLabel(self, text=str(int(current_temp)) + "°", font=("Times", 37, "bold", "italic"),
                                   text_color="#000000")
        temperature.place(relx=0.55, rely=0.47, anchor="center")

        # Max and Min temperature label
        max_and_min_temp = ctk.CTkLabel(self, text=f"H: {round(maxTemp)}°  L: {round(minTemp)}°", font=("Times", 20),
                                        text_color="#000000")
        max_and_min_temp.place(relx=0.52, rely=0.72, anchor='center')
