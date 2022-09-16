# API
import flask
from flask import request, jsonify
from flask_cors import cross_origin

# data manipulation
import requests
from datetime import datetime
import pytz
import pandas as pd

# expert system
from experta import *
from regras import *
import func

# global weather_data, temp, humidity, alturaMaior6, umidadeSolo


def get_weather_data():
    API_KEY = "4917b81e0867695458dc26cdc1daac35"
    lat = -24.2817
    lng = -53.8404

    link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&lang=pt_br"

    res = requests.get(link)
    weather_data = res.json()
    return weather_data

def get_irrigation_status(temp, umidadeAr, condClima, aux, aux2):
    engine.reset()
    engine.declare(Fact(TemperaturaAcima30=func.temperaturaAcima30(temp),
                        Temperatura20_30=func.temperatura20_30(temp),
                        Temperatura10_20=func.temperatura10_20(temp),
                        TemperaturaMinima=func.temperaturaMinima(temp),
                        UmidadeArAbaixo50=func.umidadeArAbaixo50(
                            umidadeAr),
                        UmidadeArAbaixo30=func.umidadeArAbaixo30(
                            umidadeAr),
                        UmidadeAr=func.umidadeAr50(umidadeAr),
                        TempChuva=func.tempChuva(condClima),
                        UmidadeSoloAcima60=func.UmidadeSoloAcima60(aux),
                        UmidadeSoloAbaixo60=func.UmidadeSoloAbaixo60(aux),
                        PlantaAcima6=aux2
                        ))
    engine.run()

    resultado = ret()
    resultadoP = retP()
    res = [resultado, resultadoP]

    engine.reset()


    return res


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Lupulo API</h1>"

@app.route('/irrigation', methods=['GET'])
@cross_origin()
def api_all():
    if 'secondPhase' in request.args:
        if (request.args['secondPhase'] == 'true'):
            alturaMaior6 = True
        else:
            alturaMaior6 = False
    else:
        alturaMaior6 = False


    if 'soilMoisture' in request.args:
        umidadeSolo = int(request.args['soilMoisture'])
    else:
        return "Error: 'soilMoisture' field provided."

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

    print(alturaMaior6)
    print(umidadeSolo)
    return jsonify(get_irrigation_status(
        temp,
        humidity,
        condClima,
        umidadeSolo,
        alturaMaior6,
    ))


app.run()
