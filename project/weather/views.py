from django.shortcuts import render
import requests
from .models import City
from .forms import *
from dotenv import load_dotenv
import os
from django.conf import settings


def index(request):
    
    api_key = settings.OPENWEATHER_API_KEY  # from .env
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    city = 'London'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    
    form = CityForm
    
    cities = City.objects.all()
    
    weather_data = []
    
    for city in cities:
    
        r = requests.get(url.format(city, api_key)).json()
    
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        
        weather_data.append(city_weather)
        
    
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context) #returns the index.html template

    