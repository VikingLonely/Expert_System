from email.mime import image
from turtle import color
from PySimpleGUI import PySimpleGUI as sg
from experta import *
import func
import api
from regras import *

image = 'D:/Usuário/Documents/Faculdade/IA/TrabalhoFinal/images/Blooming-bro.png'
temp = api.temp
umidadeAr = api.humidity
condClima = api.condClima

sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': 'light blue',
                                            'TEXT': 'black',
                                            'INPUT': 'white',
                                            'TEXT_INPUT': 'black',
                                            'SCROLL': 'LightBlue3',
                                            'BUTTON': ('DeepSkyBlue4', 'DeepSkyBlue3'),
                                            'PROGRESS': ('# D1826B', '# CC8019'),
                                            'BORDER': 1, 'SLIDER_DEPTH': 0,
                                            'PROGRESS_DEPTH': 0, }

layout_img = [
    [sg.Image(filename='Blooming-bro.png', background_color='light blue')]]

layout_title = [
    [sg.Push(background_color='light blue'), sg.Frame('', [[sg.Text('Irrigação - Lupulo', font=('Times new Roman', 16), background_color='light blue', text_color='black')]], background_color='LightBlue3'), sg.Push(background_color='light blue')]]

layout_umidade = [
    [sg.Frame('', [[sg.Text('Umidade do Solo: ', font=('Times new Roman', 12), background_color='LightBlue3', text_color='black')],
                   [sg.Input(key='umidadeSolo', size=(23, 1))]], background_color='LightBlue3')],
    [sg.Text(background_color='light blue')],
    [sg.Frame('', [[sg.Text("Altura da Planta: ",  font=('Times new Roman', 12), background_color='LightBlue3', text_color='black')],
                   [sg.Checkbox('6 metros ou mais', key='plantaMaior', size=(20, 2), font=(
                       'Times new Roman', 10), background_color='LightBlue3', text_color='black')],
                   [sg.Checkbox('Menor que 6 metros', key='plantaMenor',  size=(20, 2), font=(
                       'Times new Roman', 10), background_color='LightBlue3', text_color='black')]], background_color='LightBlue3')],
    [sg.Text(size=(0, 2), background_color='light blue')],
    [sg.Push(background_color='light blue'), sg.Button('Verificar Irrigação')]

]


def janela_main():
    sg.theme('MyCreatedTheme')
    layout = [
        [layout_title],
        [sg.Column(layout_img),
         sg.Column(layout_umidade)]
    ]
    return sg.Window('Main', layout=layout, finalize=True)


def janela_resul():
    sg.theme('TealMono')
    layout = [
        [sg.Text('Resposta Expert System')],
        [sg.Text('', key='resul1')],
        [sg.Text('', key='resul2')],
        [sg.Push(), sg.Push(), sg.Button('Finalizar')]
    ]
    return sg.Window('Expert System', size=(600, 400), layout=layout, finalize=True)


janela1, janela2 = janela_main(), None


while True:
    window, event, values = sg.read_all_windows()

    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela1 and event == 'Verificar Irrigação':
        aux = values['umidadeSolo']
        if(values['plantaMaior'] == True):
            aux2 = True
        if(values['plantaMenor'] == True):
            aux2 = False
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

    if window == janela2 and event == 'Finalizar' or event == sg.WIN_CLOSED:
        break

janela1.close()
janela2.close()
