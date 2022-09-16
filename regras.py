from experta import *

retorno = None
retornoP = None


def ret():
    return retorno


def retP():
    return retornoP


class InferenceEngine(KnowledgeEngine):

    # Regra 1
    # Se chover não irrigar
    @Rule(Fact(TempChuva=True), Fact(UmidadeAr=True))
    def Chuva(self):
        self.declare(Fact(IrrigacaooChuva=True))
        global retorno
        retorno = ("Clima chuvoso - não irrigar")

    # Regra 2
    # Se chover porem a umidade do ar estiver baixa então irrigar menos
    @Rule(Fact(TempChuva=True), Fact(UmidadeArAbaixo50=True))
    def poucaChuva(self):
        self.declare(Fact(IrrigacaoPoucaChuva=True))
        global retorno
        retorno = (
            "Pouco chuva e Umidade baixa - irrigar com frequencia diminida pela metade")

    # Regra 3
    # Se a temperatura estiver acima de 30° irrigar de 2 em 2 horas.
    @Rule(Fact(TemperaturaAcima30=True), Fact(TempChuva=False))
    def climaQuente(self):
        self.declare(Fact(IrrigacaoClimaQuente=True), Fact(TempChuva=False))
        global retorno
        retorno = ("Temperatura alta - Irigação será ligada de 2 em 2 horas!")

    # Regra 4
    # Se a temperatura estiver acima de 30° e umidade do ar abaixo de 30% então dobrar frequência da irrigação
    @Rule(Fact(TemperaturaAcima30=True), Fact(UmidadeArAbaixo30=True), Fact(TempChuva=False))
    def superAquecido(self):
        self.declare(Fact(IrrigacaoDobrada=True))
        global retorno
        retorno = ("Ambiente superAquecido-Irrigação será ligada de 1 em 1 hora!")

    # Regra 5
    # se a temperatura estiver entre 20° e 30° e a umidade do ar estiver abaixo de 50 % então irrigue de 2 em 2 horas
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeArAbaixo50=True), Fact(TempChuva=False))
    def TempoIdeal(self):
        self.declare(Fact(IrrigacaoNormal=True))

    # Regra 6
    # se a temperatura estiver entre 20° e 30° e a umidade do ar estiver acima de 50 % então irrigue de 4 em 4 horas
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeAr=True), Fact(TempChuva=False))
    def TempoIdeal1(self):
        self.declare(Fact(IrrigacaoBaixa=True))
        global retorno
        retorno = ("Temperatura ideal - irrigar com frequencia diminuida")

    # Regra 7
    # Se a temperatura estiver abaixo de 10° então não irrigar
    @Rule(Fact(TemperaturaMinima=True), Fact(TempChuva=False))
    def TempoFrio(self):
        self.declare(Fact(IrrigacaoFrio=True))
        global retorno
        retorno = "Clima muito frio - Não irrigar"

    # Regra 8
    # se a temperatura estiver entre 10° e 20° então irrigue só de manhã uma vez./
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeArAbaixo50=True), Fact(TempChuva=False))
    def Manha1(self):
        self.declare(Fact(IrrigacaoManha=True))

    # Regra 9
    # se a temperatura estiver entre 10° e 20° e umidade do ar acima de 50% então não irrigue.
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeAr=True), Fact(TempChuva=False))
    def Manha(self):
        self.declare(Fact(IrrigacaoManha=False))
        global retorno
        retorno = 'Temperatura Baixa - Não irá ligar irrigação'

    # Regra 10
    # se a regra 5 for verdadeira verificar a condição do solo

    @Rule(Fact(IrrigacaoNormal=True), Fact(UmidadeSoloAcima60=True))
    def SoloUmido(self):
        self.declare(Fact(IrrigacaoNormalFinal=False))
        global retorno
        retorno = ("Solo Muito umido - Não irrigar")

    # Regra 11
    @Rule(Fact(IrrigacaoNormal=True), Fact(UmidadeSoloAbaixo60=True))
    def SoloSeco(self):
        self.declare(Fact(IrrigacaoNormalFinal=True))
        global retorno
        retorno = ("Solo seco - Ligar irrigação")

    # Regra 12
    # se a regra 8 for verdadeira verificar condição do solo
    @Rule(Fact(IrrigacaoManha=True), Fact(UmidadeSoloAcima60=True))
    def SoloUmidoManha(self):
        self.declare(Fact(IrrigacaoManhaFinal=False))
        global retorno
        retorno = ("Solo Muito umido - Não irrigar")

    # Regra 13
    @Rule(Fact(IrrigacaoManha=True), Fact(UmidadeSoloAbaixo60=True))
    def SoloSecoManha(self):
        self.declare(Fact(IrrigacaoManhaFinal=True))
        global retorno
        retorno = ("Ligar irrigação só uma vez de manhã")

    # Regra 14
    @Rule(Fact(PlantaAcima6=True))
    def estagioFinal(self):
        self.declare(Fact(IrrigacaoMetade=True))
        global retornoP
        retornoP = ("Planta no estagio final - irrigar com metade do volume")

    # Regra 15
    @Rule(Fact(PlantaAcima6=False))
    def estagioFinal2(self):
        self.declare(Fact(IrrigacaoMetade=False))
        global retornoP
        retornoP = None


engine = InferenceEngine()


# Altura da planta
# Quantidade de sol diaria (em horas)
