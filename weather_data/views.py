from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests
import json
# Create your views here.


def index(request):
    # 7e8aa45bbe41c38deae3322be1744ae2
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=7e8aa45bbe41c38deae3322be1744ae2'
    context=None
    if request.method == 'POST':
        name_body = request.POST['name']
        print(name_body)

        response_weather = requests.get(
            url.format(name_body)).json()

        print(response_weather)
        if response_weather['cod'] == '404':
            pass
        else:
            form = CityForm(request.POST)
            if form.is_valid():
                form.save()
                print('success')

    elif request.method =='GET':
        
        form = CityForm()

        cities = City.objects.all()
        weather_data = []

        for city in cities:

            r = requests.get(url.format(city)).json()
            print(r)
            city_weather = {
                'city': city,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
                'country': r['sys']['country'],
            }
            weather_data.append(city_weather)
        print('weather_data : {}'.format(weather_data))
        context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)
