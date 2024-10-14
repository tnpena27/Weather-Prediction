# Weather-Prediction
### Project Course: Scripting and Programming Applications
This program is designed to retrieve historical weather data from the previous 5 years of Fort Worth, TX on the date of October 18th.
<br>

### The following inputs are required to run this program:
* latitude and longitute of Fort Worth, TX
* the month, in number form, and day of a date (October 18th = 10/18)
* previous 5 years from date (2019, 2020, 2021, 2022, 2023) 
<br>

### The following commands are inclued:
* mean(): to find the average temperature, windspeeds, and precipations from the past 5 years on October 18th.
* min(): to find the minimum temperature, windspeeds, and precipations from the past 5 years on October 18th.
* max(): to find the maximum temperature, windspeeds, and precipations from the past 5 years on October 18th.
* c = conn.cursor(): cursor
* conn = sqlite3.connect(): to connect to sqlite database
* c.execute(): to execute SQL statements within python
* conn.commit(): to commit changes within the sqlite database
* conn.close(): to close the connection to sqlite database
* test_function(): a test function must start with test_ to intialize a unit test
<br>

### The following outputs will result from this code:
**From main.py**
* latitude
* longitude
* month
* day of month
* years
* five-year average temperature
* five-year minimum temperature
* five-year maximum temperature
* five-year average windspeed
* five-year minimum windspeed
* five-year maximum windspeed
* five-year sum precipitation
* five-year minimum precipitation
* five-year maximum precipitation
* A set of data that includes the maximum temperature, maximum windspeed, and precipitation sum for each of the five years.

**From database.py**
* A table created in sqlite3 that stores the data retrieved from the WeatherData class in main.py

**From test.py**
* Output will show that 3 unit tests have successfully been ran.
