from PySimpleGUI import PySimpleGUI as sg
from experta import *
import func
import api

from regras import *

temp = api.temp
umidadeAr = api.humidity
condClima = api.condClima


def janela_main():
    sg.theme('TealMono')
    layout = [
        [sg.Push(), sg.Text(
            'Irrigação - Lupulo'), sg.Push()],
        [sg.Text('Nível de umidade do solo (%):'),
         sg.Input(key='umidadeSolo', size=(5, 1))],
        [sg.Checkbox('Lupulo com ou mais de 6 metros?', key='alturaPlanta')],
        [sg.Button('Verificar Irrigação')]
    ]
    return sg.Window('Main', layout=layout, finalize=True)


def janela_resul():
    sg.theme('TealMono')
    layout = [
        [sg.Text('Resposta Expert System')],
        [sg.Text('', key='resul1')],
        [sg.Text('', key='resul2')],
        [sg.Button('Voltar'), sg.Push(), sg.Button('Finalizar')]
    ]
    return sg.Window('Expert System', layout=layout, finalize=True)


janela1, janela2 = janela_main(), None


while True:
    window, event, values = sg.read_all_windows()

    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela1 and event == 'Verificar Irrigação':
        aux = values['umidadeSolo']
        aux2 = values['alturaPlanta']
        janela2 = janela_resul()
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
        janela2['resul1'].update(f'{resultado}')
        if(resultadoP == None):
            janela2['resul2'].update('Planta em fase de crescimento!')
        else:
            janela2['resul2'].update(f'{resultadoP}')
        janela1.hide()

    if window == janela2 and event == 'Voltar':
        engine.reset()
        janela2.hide()
        janela1.un_hide()

    if window == janela2 and event == 'Finalizar' or event == sg.WIN_CLOSED:
        break

janela1.close()
janela2.close()
