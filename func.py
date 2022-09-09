def temperaturaAcima30(temp):
    return temp >= 30


def temperaturaMinima(temp):
    return temp <= 10


def umidadeAr50(umidadeAr):
    return umidadeAr >= 50


def umidadeArAbaixo50(umidadeAr):
    return 30 < umidadeAr < 50


def umidadeArAbaixo30(umidadeAr):
    return umidadeAr < 30


def luzIdeal(luz):
    return luz >= 17


def temperatura20_30(temp):
    return temp >= 20 and temp < 30


def tempChuva(clima):
    return (clima == 'Rain' or clima == 'Thunderstorm' or clima == 'Drizzle' or clima == 'Snow')


def UmidadeSoloAcima60(UmidadeSolo):
    return UmidadeSolo >= 60


def UmidadeSoloAbaixo60(UmidadeSolo):
    return UmidadeSolo < 60
