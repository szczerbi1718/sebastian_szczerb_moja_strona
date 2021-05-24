import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from datetime import datetime


def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fedf67683eebe39de4b607c9cee91978&lang=pl'

    err_msg = ''
    message = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'To miasto nie istnieje'
            else:
                err_msg = 'Miasto juz jest dodane w Pogodzie!'

        if err_msg:
            message = err_msg
        else:
            message = 'Miasto zostało dodane'



    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        weather_city = {
            'city' : city.name,
            'description' : r['weather'][0]['description'],
            'ikonka': r['weather'][0]['icon'],
            'temperature' : r['main']['temp'],
            'temperatura_odczuwalna': r['main']['feels_like'],
            'temperatura_minimalna': r['main']['temp_min'],
            'temperatura_maksymalna': r['main']['temp_max'],
            'cisnienie': r['main']['pressure'],
            'wilgotnosc': r['main']['humidity'],
            'wiatr': r['wind']['speed'],
            'wschod': datetime.utcfromtimestamp(int(r['sys']['sunrise'])).strftime('%Y-%m-%d o godzinie -  %H:%M:%S'),
            'zachod': datetime.utcfromtimestamp(int(r['sys']['sunset'])).strftime('%Y-%m-%d o godzinie -  %H:%M:%S'),


        }

        weather_data.append(weather_city)

    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message
    }

    return render(request, 'weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('weather')
