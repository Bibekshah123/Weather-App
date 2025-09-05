from django.shortcuts import render
import requests
from .models import City
from .forms import *
from dotenv import load_dotenv
import os

def index(request):
    
    load_dotenv()
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set OPENWEATHER_API_KEY in your environment or .env file.")
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={api_key}'

    cities = City.objects.all() #return all the cities in the database
    
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    
    form = CityForm
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city))
        if response.status_code == 404:
            continue
        city_weather = response.json()

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form': form}


    return render(request, 'weather/index.html') #returns the index.html template