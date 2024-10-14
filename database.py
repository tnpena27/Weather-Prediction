# This file creates a database to hold the 5-year weather data for Fort Worth, TX on October 18th.

import sqlite3
import requests
from statistics import mean

# Creates WeatherData class
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

    # Defines function to fetch weather data
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

    # Defines function to fetch data for a date
    def fetch_data_for_date(self, date):
        url = (f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}"
               f"&start_date={date}&end_date={date}&daily=temperature_2m_max,wind_speed_10m_max,precipitation_sum"
               "&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch")
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

def retrieve_weather_data(db_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Query the database
    c.execute("SELECT * FROM fortWorthWeather")
    rows = c.fetchall()

    # Fetch column names
    column_names = [description[0] for description in c.description]

    # Close the connection
    conn.close()

    return column_names, rows

# Displays table vertically
def display_data_vertically(column_names, rows):
    for row in rows:
        row_dict = dict(zip(column_names, row))
        for key, value in row_dict.items():
            print(f"{key}: {value}")
        print()  # Print a newline for better readability

# Define the years, month, and day
years = [2019, 2020, 2021, 2022, 2023]
month = 10
day = 18
latitude = 32.7555
longitude = -97.3308

# Create an instance of the WeatherData class
fort_worth_weather = WeatherData(latitude, longitude, month, day, years)

# Connect to the SQLite database
conn = sqlite3.connect('main.db')
c = conn.cursor()

# Drop the table if it exists
c.execute("DROP TABLE IF EXISTS fortWorthWeather")

# Create table with correct schema
c.execute("""CREATE TABLE fortWorthWeather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_latitude REAL,
            location_longitude REAL,
            month INTEGER,
            day_of_month INTEGER,
            five_yr_avg_temp FLOAT,
            five_yr_min_temp FLOAT,
            five_yr_max_temp FLOAT,
            five_yr_avg_wind_speed FLOAT,
            five_yr_min_wind_speed FLOAT,
            five_yr_max_wind_speed FLOAT,
            five_yr_sum_precip FLOAT,
            five_yr_min_precip FLOAT,
            five_yr_max_precip FLOAT
            )""")

# Insert data into the database
c.execute("""INSERT INTO fortWorthWeather (
            location_latitude, location_longitude, month, day_of_month, 
            five_yr_avg_temp, five_yr_min_temp, five_yr_max_temp, 
            five_yr_avg_wind_speed, five_yr_min_wind_speed, five_yr_max_wind_speed, 
            five_yr_sum_precip, five_yr_min_precip, five_yr_max_precip)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
          (fort_worth_weather.latitude, fort_worth_weather.longitude, fort_worth_weather.month, fort_worth_weather.day,
           fort_worth_weather.avg_temperature, fort_worth_weather.min_temperature, fort_worth_weather.max_temperature,
           fort_worth_weather.avg_wind_speed, fort_worth_weather.min_wind_speed, fort_worth_weather.max_wind_speed,
           fort_worth_weather.sum_precipitation, fort_worth_weather.min_precipitation, fort_worth_weather.max_precipitation))

# Commit and close the connection
conn.commit()
conn.close()

# Retrieve and print the stored weather data with column names
column_names, weather_data = retrieve_weather_data('main.db')

# Display the results vertically
display_data_vertically(column_names, weather_data)
