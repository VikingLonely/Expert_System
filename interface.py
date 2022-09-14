from PySimpleGUI import PySimpleGUI as sg


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
        [sg.Button('Voltar a tela inicial'), sg.Push(), sg.Button('Finalizar')]
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
        janela1.hide()
    if window == janela2 and event == 'Voltar a tela inicial':
        janela2.hide()
        janela1.un_hide()
    if window == janela2 and event == 'Finalizar' or event == sg.WIN_CLOSED:
        break

janela1.close()
janela2.close()
