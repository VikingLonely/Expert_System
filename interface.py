
from PySimpleGUI import PySimpleGUI as sg
from experta import *
import func
import api
from regras import *

temp = api.temp
umidadeAr = api.humidity
condClima = api.condClima

# Cria um tema para a interface
sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': 'light blue',
                                            'TEXT': 'black',
                                            'INPUT': 'white',
                                            'TEXT_INPUT': 'black',
                                            'SCROLL': 'LightBlue3',
                                            'BUTTON': ('DeepSkyBlue4', 'DeepSkyBlue3'),
                                            'PROGRESS': ('# D1826B', '# CC8019'),
                                            'BORDER': 1, 'SLIDER_DEPTH': 0,
                                            'PROGRESS_DEPTH': 0, }

# Criaçao do layout da img da tela principal e de resposta
layout_imgMain = [
    [sg.Image(filename='Blooming-bro.png', background_color='light blue')]]

layout_imgR = [
    [sg.Image(filename='Water_drop-bro.png', background_color='light blue')]
]

# criaçao do layout do titulo da tela principal e de resposta
layout_titleMain = [
    [sg.Push(background_color='light blue'), sg.Frame('', [[sg.Text('Irrigação - Lupulo', font=('Times new Roman', 16), background_color='light blue', text_color='black')]], background_color='LightBlue3'), sg.Push(background_color='light blue')]]

layout_titleR = [
    [sg.Push(background_color='light blue'), sg.Frame('', [[sg.Text('Expert System', font=('Times new Roman', 16),
                                                                    background_color='light blue', text_color='black')]], background_color='LightBlue3'), sg.Push(background_color='light blue')]
]

# Criaçao dos campos de variaveis da tela principal
layout_variaveis = [
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

# criaçao dos campos onde vão ser apresntados as respostas
layout_Resp = [
    [sg.Text(background_color='light blue')],
    [sg.Frame('', [[sg.Text('Resposta:', font=('Times new Roman', 12), background_color='LightBlue3', text_color='black')],
                   [sg.Text('', key='resul1', background_color='white', size=(35, 3), text_color='black')]], background_color='LightBlue3')],
    [sg.Text(background_color='light blue')],
    [sg.Frame('', [[sg.Text('Obs:', font=('Times new Roman', 12),
              background_color='LightBlue3', text_color='black')],
                   [sg.Text('', key='resul2', background_color='white', size=(35, 3), text_color='black')]], background_color='LightBlue3')],
    [sg.Text(size=(0, 2), background_color='light blue')],
    [sg.Push(background_color='light blue'),
     sg.Button('Finalizar')]
]

# organizaçao do janela Main


def janela_main():
    sg.theme('MyCreatedTheme')
    layout = [
        [layout_titleMain],
        [sg.Column(layout_imgMain),
         sg.Column(layout_variaveis)]
    ]
    return sg.Window('Main', layout=layout, finalize=True)

# Organizaçao  da janela de resposta


def janela_resul():
    sg.theme('MyCreatedTheme')
    layout = [
        [layout_titleR],
        [sg.Column(layout_imgR),
         sg.Column(layout_Resp)]
    ]
    return sg.Window('Expert System', layout=layout, finalize=True)


# inicialização da tela principal
janela1, janela2 = janela_main(), None

# logica da interface
while True:
    # funcão que le tudo que acontece nas janelas
    window, event, values = sg.read_all_windows()

    # condiçao inicial de parada
    if window == janela1 and event == sg.WIN_CLOSED:
        break

    # funcão que irá coletar os valores das variaveis e iniciar as regras para buscar uma resposta
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
        janela2['resul1'].update(f' {resultado}')
        if(resultadoP == None):
            janela2['resul2'].update(' Planta em fase de crescimento!' +
                                     ' A irrigação será normal.')
        else:
            janela2['resul2'].update(f'{resultadoP}')
        janela1.hide()

    # segunda condiçao de parada
    if window == janela2 and event == 'Finalizar' or event == sg.WIN_CLOSED:
        break

# finalizaçao das janelas
janela1.close()
janela2.close()
