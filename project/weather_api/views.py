from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from weather.models import City
from .serializers import CitySerializer
import requests


# List and Create Cities
class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


# Delete a City
class CityDeleteView(generics.DestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = "pk"


# Get Weather for a City
class WeatherDetailView(APIView):
    def get(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

        api_key = settings.OPENWEATHER_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={api_key}"

        r = requests.get(url).json()

        if "main" not in r:
            return Response({"error": "Weather data not found"}, status=status.HTTP_404_NOT_FOUND)

        weather_data = {
            "city": city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }
        return Response(weather_data)
