import requests


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
temp = weather_data['main']['temp'] - 273.15
humidity = weather_data['main']['humidity']

print("{:<18} {:<18}".format("Temperatura", temp))
print("{:<18} {:<18}".format("Umidade", humidity))

# Definicao de variavies
tempAcima30 = temp >= 30
print(tempAcima30)
