# This file executes 3 test for the database.py file.

import unittest
import sqlite3
import os
from database import WeatherData, retrieve_weather_data, display_data_vertically

# Creates TestWeatherData class
class TestWeatherData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_main.db'
        # Define the years, month, and day for the tests
        cls.years = [2019, 2020, 2021, 2022, 2023]
        cls.month = 10
        cls.day = 18
        cls.latitude = 32.7555
        cls.longitude = -97.3308

        # Create an instance of the WeatherData class
        cls.weather_data = WeatherData(cls.latitude, cls.longitude, cls.month, cls.day, cls.years)

        # Connect to the SQLite database
        conn = sqlite3.connect(cls.db_name)
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
                  (cls.weather_data.latitude, cls.weather_data.longitude, cls.weather_data.month, cls.weather_data.day,
                   cls.weather_data.avg_temperature, cls.weather_data.min_temperature, cls.weather_data.max_temperature,
                   cls.weather_data.avg_wind_speed, cls.weather_data.min_wind_speed, cls.weather_data.max_wind_speed,
                   cls.weather_data.sum_precipitation, cls.weather_data.min_precipitation, cls.weather_data.max_precipitation))

        # Commit and close the connection
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Remove the test database file
        os.remove(cls.db_name)

    # Checks if the WeatherData object is correctly initialized
    def test_weather_data_initialization(self):
        self.assertEqual(self.weather_data.latitude, 32.7555)
        self.assertEqual(self.weather_data.longitude, -97.3308)
        self.assertEqual(self.weather_data.month, 10)
        self.assertEqual(self.weather_data.day, 18)
        self.assertEqual(self.weather_data.years, [2019, 2020, 2021, 2022, 2023])
        self.assertIsNotNone(self.weather_data.avg_temperature)
        self.assertIsNotNone(self.weather_data.min_temperature)
        self.assertIsNotNone(self.weather_data.max_temperature)
        self.assertIsNotNone(self.weather_data.avg_wind_speed)
        self.assertIsNotNone(self.weather_data.min_wind_speed)
        self.assertIsNotNone(self.weather_data.max_wind_speed)
        self.assertIsNotNone(self.weather_data.sum_precipitation)
        self.assertIsNotNone(self.weather_data.min_precipitation)
        self.assertIsNotNone(self.weather_data.max_precipitation)

    # Verifies that the weather data is accurately inserted into the SQLite database
    def test_database_insertion(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM fortWorthWeather")
        rows = c.fetchall()
        conn.close()

        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row[1], self.weather_data.latitude)
        self.assertEqual(row[2], self.weather_data.longitude)
        self.assertEqual(row[3], self.weather_data.month)
        self.assertEqual(row[4], self.weather_data.day)
        self.assertEqual(row[5], self.weather_data.avg_temperature)
        self.assertEqual(row[6], self.weather_data.min_temperature)
        self.assertEqual(row[7], self.weather_data.max_temperature)
        self.assertEqual(row[8], self.weather_data.avg_wind_speed)
        self.assertEqual(row[9], self.weather_data.min_wind_speed)
        self.assertEqual(row[10], self.weather_data.max_wind_speed)
        self.assertEqual(row[11], self.weather_data.sum_precipitation)
        self.assertEqual(row[12], self.weather_data.min_precipitation)
        self.assertEqual(row[13], self.weather_data.max_precipitation)

    # Confirms data can be correctly retrieved from database and that it matches the original weather data attributes
    def test_retrieve_weather_data(self):
        column_names, rows = retrieve_weather_data(self.db_name)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        row_dict = dict(zip(column_names, row))
        self.assertEqual(row_dict['location_latitude'], self.weather_data.latitude)
        self.assertEqual(row_dict['location_longitude'], self.weather_data.longitude)
        self.assertEqual(row_dict['month'], self.weather_data.month)
        self.assertEqual(row_dict['day_of_month'], self.weather_data.day)
        self.assertEqual(row_dict['five_yr_avg_temp'], self.weather_data.avg_temperature)
        self.assertEqual(row_dict['five_yr_min_temp'], self.weather_data.min_temperature)
        self.assertEqual(row_dict['five_yr_max_temp'], self.weather_data.max_temperature)
        self.assertEqual(row_dict['five_yr_avg_wind_speed'], self.weather_data.avg_wind_speed)
