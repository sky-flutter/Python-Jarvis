import requests, json
import math
import config


class Weather:
    weatherURL = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"
    currentCity = "Ahmedabad"
    locationKey = "202438"

    def __init__(self, cityName="Ahmedabad"):
        self.currentCity = cityName

    def getLocationKey(self):
        if self.currentCity.lower() != "ahmedabad" or self.currentCity.lower() != "amdavad":
            location = (
                "http://dataservice.accuweather.com/locations/v1/cities/search?apikey="
                + config.weather_key
                + "&q="
                + self.currentCity
            )
            locationResponse = requests.get(location)
            locationResponse = locationResponse.json()
            try:
                if locationResponse[0]["Key"] is not None:
                    self.locationKey = locationResponse[0]["Key"]
                    return self.getWeather()
                else:
                    return "Could not find weather data"

            except Exception as e:
                return "Could not find weather data"
        else:
            return self.getWeather()

    def getWeather(self):
        self.weatherURL = self.weatherURL + self.locationKey + "?apikey=" + config.weather_key
        responses = requests.get(self.weatherURL)
        weatherData = responses.json()
        try:
            if weatherData[0]["Temperature"] is not None:
                tempFahrenHeit = weatherData[0]["Temperature"]['Value']
                tempCelcius = (tempFahrenHeit - 32) * 5/9
                tempCelcius = round(tempCelcius)
                return "Today's temperature is {0} Celcius".format(tempCelcius)
            else:
                return "Could not find weather data"

        except Exception as e:
            return "Could not find weather data"