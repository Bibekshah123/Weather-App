from django.urls import path
from .views import *

urlpatterns = [
    path("api/cities/", CityListCreateView.as_view(), name="city_list_create"),
    path("api/cities/<int:pk>/delete/", CityDeleteView.as_view(), name="city_delete"),
    path("api/weather/<int:pk>/", WeatherDetailView.as_view(), name="weather_detail"),
]
