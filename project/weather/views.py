from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import City
from .forms import *
from dotenv import load_dotenv
import os
from django.conf import settings


def index(request):
    
    api_key = settings.OPENWEATHER_API_KEY  # from .env
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    city = 'London'
    
    if request.method == 'POST' and 'name' in request.POST:
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    
    form = CityForm
    
    cities = City.objects.all()
    
    weather_data = []
    
    for city in cities:
    
        r = requests.get(url.format(city, api_key)).json()
        
         #Check if API returned valid data
        if r.get("cod") != 200:
            print(f"Error fetching {city.name}: {r.get('message')}")
            continue  # skip this city if not found or error
    
        city_weather = {
            'id': city.id,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        
        weather_data.append(city_weather)
        
    
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context) #returns the index.html template


def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect('index')