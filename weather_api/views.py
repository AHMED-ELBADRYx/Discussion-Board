from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


# def weather(request):
#     url = 'http://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
#     errors = []
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         form.save()

#     form = CityForm()
#     cities = City.objects.all()
#     weather_data = []
    
#     if cities:
#         for city in cities:
#             data_url = url + city.name
#             response = requests.get(data_url).json()
#             if 'main' in response and 'weather' in response:
#                 city_weather = {
#                     'city': city.name,
#                     'temperature': response['main']['temp'],
#                     'description': response['weather'][0]['description'],
#                     'icon': response['weather'][0]['icon'],
#                 }
#                 weather_data.append(city_weather)

#             else:
#                 error_msg = response.get('message', 'No data found')
#                 errors.append(f"{city.name}: {error_msg}")
#                 city_weather = {
#                     'city': city.name,
#                     'temperature': 'N/A',
#                     'description': error_msg,
#                     'icon': '',
#                 }
#                 weather_data.append(city_weather)

#     return render(request, 'weather_api/weather.html', {'weather_data': weather_data, 'form': form, 'errors': errors})

def weather(request):
    url = 'http://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    errors = []
    weather_data = []
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            data_url = url + city_name
            response = requests.get(data_url).json()
            if 'main' in response and 'weather' in response:
                city_weather = {
                    'city': city_name,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                }
                weather_data.append(city_weather)
            else:
                error_msg = response.get('message', 'No data found')
                errors.append(f"{city_name}: {error_msg}")
        # لا تحفظ المدينة في قاعدة البيانات
    else:
        form = CityForm()

    return render(request, 'weather_api/weather.html', {
        'weather_data': weather_data,
        'form': form,
        'errors': errors[-1:]  # فقط آخر رسالة خطأ
    })