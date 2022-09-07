
from experta import *
import func
import api

temp = api.temp
umidadeAr = api.humidity
condClima = api.condClima


class InferenceEngine(KnowledgeEngine):
    @Rule(Fact(TempChuva=True), Fact(UmidadeAr=True))
    def Chuva(self):
        self.declare(Fact(IrrigacaooChuva=True))
        print("Clima chuvoso - não irrigar")

    @Rule(Fact(TempChuva=True), Fact(UmidadeArAbaixo50=True))
    def poucaChuva(self):
        self.declare(Fact(IrrigacaoPoucaChuva=True))
        print("Pouco chuva e Umidade baixa - irrigar com frequencia diminida pela metade")

    # Se a temperatura estiver acima de 30° irrigar de 2 em 2 horas.
    @Rule(Fact(TemperaturaAcima30=True), Fact(TempChuva=False))
    def climaQuente(self):
        self.declare(Fact(IrrigacaoClimaQuente=True), Fact(TempChuva=False))
        print("Temperatura alta - Irigação será ligada de 2 em 2 horas!")

    # Se a temperatura estiver acima de 30° e umidade do ar abaixo de 30% então dobrar frequência da irrigação
    @Rule(Fact(TemperaturaAcima30=True), Fact(UmidadeArAbaixo30=True), Fact(TempChuva=False))
    def superAquecido(self):
        self.declare(Fact(IrrigacaoDobrada=True))
        print("Ambiente superAquecido-Irrigação será ligada de 1 em 1 hora!")

    # se a temperatura estiver entre 20° e 30° e a umidade do ar estiver abaixo de 50 % então irrigue de 2 em 2 horas
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeArAbaixo50=True), Fact(TempChuva=False))
    def TempoSeco(self):
        self.declare(Fact(IrrigacaoNormal=True))

    # se a temperatura estiver entre 20° e 30° e a umidade do ar estiver acima de 50 % então irrigue de 4 em 4 horas
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeAr=True), Fact(TempChuva=False))
    def TempoSeco(self):
        self.declare(Fact(IrrigacaoBaixa=True))

    # Se a temperatura estiver abaixo de 10° então não irrigar.

    @Rule(Fact(TemperaturaMinima=True), Fact(TempChuva=False))
    def TempoFrio(self):
        self.declare(Fact(IrrigacaoFrio=True))
        print("Clima muito frio - Não irrigar")

    # se a temperatura estiver entre 10° e 20° então irrigue só de manhã uma vez./
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeArAbaixo50=True), Fact(TempChuva=False))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManha=True))

    # se a temperatura estiver entre 10° e 20° e umidade do ar acima de 50% então não irrigue.

    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeAr=True), Fact(TempChuva=False))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManha=False))
        print("Temperatura baixa - Não será ligada a irrigação!")

    @Rule(Fact(IrrigacaoNormal=True), Fact(UmidadeSoloAcima60=True))
    def SoloUmido(self):
        self.declare(Fact(IrrigacaoNormalFinal=False))
        print("Solo Muito umido - Não irrigar")

    @Rule(Fact(IrrigacaoNormal=True), Fact(UmidadeSoloAbaixo60=True))
    def SoloSeco(self):
        self.declare(Fact(IrrigacaoNormalFinal=True))
        print("Solo seco - Ligar irrigação")

    @Rule(Fact(IrrigacaoManha=True), Fact(UmidadeSoloAcima60=True))
    def SoloUmidoManha(self):
        self.declare(Fact(IrrigacaoManhaFinal=False))
        print("Solo Muito umido - Não irrigar")

    @Rule(Fact(IrrigacaoManha=True), Fact(UmidadeSoloAbaixo60=True))
    def SoloSecoManha(self):
        self.declare(Fact(IrrigacaoManhaFinal=True))
        print("Ligar irrigação só uma vez de manhã")

    @Rule(Fact(IrrigacaoBaixa=True), Fact(UmidadeSoloAcima60=True))
    def SoloUmidoBaixa(self):
        self.declare(Fact(IrrigacaoBaixaFinal=False))
        print("Solo Muito umido - Não irrigar")

    @Rule(Fact(IrrigacaoBaixa=True), Fact(UmidadeSoloAbaixo60=True))
    def SoloSecoBaixa(self):
        self.declare(Fact(IrrigacaoBaixaFinal=True))
        print("Ligar irrigação com frequencia diminuida pela metade!")


engine = InferenceEngine()


engine.declare(Fact(TemperaturaAcima30=func.temperaturaAcima30(temp),
                    Temperatura20_30=func.temperatura20_30(temp),
                    UmidadeArAbaixo50=func.umidadeArAbaixo50(umidadeAr),
                    UmidadeArAbaixo30=func.umidadeArAbaixo30(umidadeAr),
                    UmidadeAr=func.umidadeAr50(umidadeAr),
                    TemperaturaMinima=func.temperaturaMinima(temp),
                    TempChuva=func.tempChuva(condClima),
                    UmidadeSoloAcima60=False,
                    UmidadeSoloAbaixo60=True
                    ))

# Altura da planta

# Quantidade de sol diaria (em horas)

engine.run()
engine.reset()
