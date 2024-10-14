# This file imports the 5-year weather data for Fort Worth, TX on October 18th.

import requests
from statistics import mean

# Creates WeatherData class with instance variables for Oct 18th
class WeatherData:
    def __init__(self, latitude, longitude, month, day, years):
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.years = years
        self.dates = [f"{year}-{month:02d}-{day:02d}" for year in years]
        self.temperatures = []
        self.wind_speeds = []
        self.precipitations = []

        self.fetch_weather_data()

        self.avg_temperature = mean(self.temperatures) if self.temperatures else None
        self.min_temperature = min(self.temperatures) if self.temperatures else None
        self.max_temperature = max(self.temperatures) if self.temperatures else None

        self.avg_wind_speed = mean(self.wind_speeds) if self.wind_speeds else None
        self.min_wind_speed = min(self.wind_speeds) if self.wind_speeds else None
        self.max_wind_speed = max(self.wind_speeds) if self.wind_speeds else None

        self.sum_precipitation = sum(self.precipitations) if self.precipitations else None
        self.min_precipitation = min(self.precipitations) if self.precipitations else None
        self.max_precipitation = max(self.precipitations) if self.precipitations else None

    # Defines function to fetches weather data
    def fetch_weather_data(self):
        for date in self.dates:
            data = self.fetch_data_for_date(date)
            if data and 'daily' in data:
                daily_data = data['daily']
                if 'temperature_2m_max' in daily_data:
                    self.temperatures.append(daily_data['temperature_2m_max'][0])
                if 'wind_speed_10m_max' in daily_data:
                    self.wind_speeds.append(daily_data['wind_speed_10m_max'][0])
                if 'precipitation_sum' in daily_data:
                    self.precipitations.append(daily_data['precipitation_sum'][0])

    def fetch_data_for_date(self, date):
        url = (f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}"
               f"&start_date={date}&end_date={date}&daily=temperature_2m_max,wind_speed_10m_max,precipitation_sum"
               "&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch")
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


# Define the years, month, and day
years = [2019, 2020, 2021, 2022, 2023]
month = 10
day = 18
latitude = 32.7555
longitude = -97.3308

# Create an instance of the WeatherData class
fort_worth_weather = WeatherData(latitude, longitude, month, day, years)

# Print the instance variables
print(f"Location Latitude: {fort_worth_weather.latitude}")
print(f"Location Longitude: {fort_worth_weather.longitude}")
print(f"Month: {fort_worth_weather.month}")
print(f"Day of Month: {fort_worth_weather.day}")
print(f"Years: {fort_worth_weather.years}")
print(f"Five-Year Average Temperature on October 18th: {fort_worth_weather.avg_temperature}°F")
print(f"Five-Year Minimum Temperature on October 18th: {fort_worth_weather.min_temperature}°F")
print(f"Five-Year Maximum Temperature on October 18th: {fort_worth_weather.max_temperature}°F")
print(f"Five-Year Average Wind Speed on October 18th: {fort_worth_weather.avg_wind_speed} mph")
print(f"Five-Year Minimum Wind Speed on October 18th: {fort_worth_weather.min_wind_speed} mph")
print(f"Five-Year Maximum Wind Speed on October 18th: {fort_worth_weather.max_wind_speed} mph")
print(f"Five-Year Sum Precipitation on October 18th: {fort_worth_weather.sum_precipitation} inches")
print(f"Five-Year Minimum Precipitation on October 18th: {fort_worth_weather.min_precipitation} inches")
print(f"Five-Year Maximum Precipitation on October 18th: {fort_worth_weather.max_precipitation} inches")
print("\n")

# Define the dates and the location coordinates for Fort Worth, TX
dates = ['2019-10-18', '2020-10-18', '2021-10-18', '2022-10-18', '2023-10-18']

# Function to fetch weather data for a specific date
def fetch_weather_data(date):
    url = (f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}"
           f"&start_date={date}&end_date={date}&daily=temperature_2m_max,wind_speed_10m_max,precipitation_sum"
           "&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Fetch weather data for each date
weather_data = []
for date in dates:
    data = fetch_weather_data(date)
    if data and 'daily' in data:
        daily_data = data['daily']
        weather_info = {
            'date': date,
            'max_temperature': daily_data['temperature_2m_max'][0] if 'temperature_2m_max' in daily_data else None,
            'max_wind_speed': daily_data['wind_speed_10m_max'][0] if 'wind_speed_10m_max' in daily_data else None,
            'precipitation_sum': daily_data['precipitation_sum'][0] if 'precipitation_sum' in daily_data else None
        }
        weather_data.append(weather_info)
    else:
        weather_data.append({'date': date, 'max_temperature': None, 'max_wind_speed': None, 'precipitation_sum': None})

# Print the fetched weather data
for entry in weather_data:
    print(f"Date: {entry['date']}, Max Temperature: {entry['max_temperature']}°F, Max Wind Speed: {entry['max_wind_speed']} mph, Precipitation Sum: {entry['precipitation_sum']} inches")
