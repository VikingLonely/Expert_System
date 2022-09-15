import requests
from datetime import datetime
import pytz
import pandas as pd

def get_weather_data():
    API_KEY = "4917b81e0867695458dc26cdc1daac35"
    lat = -24.2817
    lng = -53.8404

    link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&lang=pt_br"

    res = requests.get(link)
    weather_data = res.json()
    return weather_data


global weather_data, temp, humidity
weather_data = get_weather_data()

nascerSol = weather_data['sys']['sunrise']
morrerSol = weather_data['sys']['sunset']
dt_start = datetime.fromtimestamp(nascerSol, pytz.timezone('America/Sao_Paulo'))
dt_end = datetime.fromtimestamp(morrerSol, pytz.timezone('America/Sao_Paulo'))

# API variables
temp = weather_data['main']['temp'] - 273.15
humidity = weather_data['main']['humidity']
condClima = weather_data['weather'][0]['main']
quantidade_sol_diaria = (pd.date_range(dt_start, dt_end, freq="1H").strftime('%H')).array.size

print(quantidade_sol_diaria)