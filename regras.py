
from experta import *
import func
import api

temp = api.temp
umidadeAr = api.humidity
condClima = api.condClima


class InferenceEngine(KnowledgeEngine):
    # Regra 1
    # Se chover não irrigar
    @Rule(Fact(TempChuva=True), Fact(UmidadeAr=True))
    def Chuva(self):
        self.declare(Fact(IrrigacaooChuva=True))
        print("Clima chuvoso - não irrigar")

    # Regra 2
    # Se chover porem a umidade do ar estiver baixa então irrigar menos
    @Rule(Fact(TempChuva=True), Fact(UmidadeArAbaixo50=True))
    def poucaChuva(self):
        self.declare(Fact(IrrigacaoPoucaChuva=True))
        print("Pouco chuva e Umidade baixa - irrigar com frequencia diminida pela metade")

    # Regra 3
    # Se a temperatura estiver acima de 30° irrigar de 2 em 2 horas.
    @Rule(Fact(TemperaturaAcima30=True), Fact(TempChuva=False),
          Fact(PlantaAcima6=False))
    def climaQuente(self):
        self.declare(Fact(IrrigacaoClimaQuente=True), Fact(TempChuva=False))
        print("Temperatura alta - Irigação será ligada de 2 em 2 horas!")

    # Regra 4
    # Se a temperatura estiver acima de 30° e umidade do ar abaixo de 30% então dobrar frequência da irrigação
    @Rule(Fact(TemperaturaAcima30=True), Fact(UmidadeArAbaixo30=True),
          Fact(TempChuva=False), Fact(PlantaAcima6=False))
    def superAquecido(self):
        self.declare(Fact(IrrigacaoDobrada=True))
        print("Ambiente superAquecido-Irrigação será ligada de 1 em 1 hora!")

    # Regra 5
    # se a temperatura estiver entre 20° e 30° e a umidade do ar estiver abaixo de 50 % então irrigue de 2 em 2 horas
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeArAbaixo50=True),
          Fact(TempChuva=False), Fact(PlantaAcima6=False))
    def TempoSeco(self):
        self.declare(Fact(IrrigacaoNormal=True))

    # Regra 6
    # se a temperatura estiver entre 20° e 30° e a umidade do ar estiver acima de 50 % então irrigue de 4 em 4 horas
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeAr=True),
          Fact(TempChuva=False), Fact(PlantaAcima6=False))
    def TempoSeco(self):
        self.declare(Fact(IrrigacaoBaixa=True))

    # Regra 7
    # Se a temperatura estiver abaixo de 10° então não irrigar
    @Rule(Fact(TemperaturaMinima=True), Fact(TempChuva=False),
          Fact(PlantaAcima6=False))
    def TempoFrio(self):
        self.declare(Fact(IrrigacaoFrio=True))
        print("Clima muito frio - Não irrigar")

    # Regra 8
    # se a temperatura estiver entre 10° e 20° então irrigue só de manhã uma vez./
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeArAbaixo50=True),
           Fact(TempChuva=False), Fact(PlantaAcima6=False))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManha=True))

    # Regra 9
    # se a temperatura estiver entre 10° e 20° e umidade do ar acima de 50% então não irrigue.
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeAr=True),
           Fact(TempChuva=False), Fact(PlantaAcima6=False))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManha=False))
        print("Temperatura baixa - Não será ligada a irrigação!")

    # Regra 10
    # se a regra 5 for verdadeira verificar a condição do solo
    @Rule(Fact(IrrigacaoNormal=True), Fact(UmidadeSoloAcima60=True),
          Fact(PlantaAcima6=False))
    def SoloUmido(self):
        self.declare(Fact(IrrigacaoNormalFinal=False))
        print("Solo Muito umido - Não irrigar")

    # Regra 11
    @Rule(Fact(IrrigacaoNormal=True), Fact(UmidadeSoloAbaixo60=True),
          Fact(PlantaAcima6=False))
    def SoloSeco(self):
        self.declare(Fact(IrrigacaoNormalFinal=True))
        print("Solo seco - Ligar irrigação")

    # Regra 12
    # se a regra 8 for verdadeira verificar condição do solo
    @Rule(Fact(IrrigacaoManha=True), Fact(UmidadeSoloAcima60=True),
          Fact(PlantaAcima6=False))
    def SoloUmidoManha(self):
        self.declare(Fact(IrrigacaoManhaFinal=False))
        print("Solo Muito umido - Não irrigar")

    # Regra 13
    @Rule(Fact(IrrigacaoManha=True), Fact(UmidadeSoloAbaixo60=True),
          Fact(PlantaAcima6=False))
    def SoloSecoManha(self):
        self.declare(Fact(IrrigacaoManhaFinal=True))
        print("Ligar irrigação só uma vez de manhã")

    # Regra 14
    # Se a regra 6 for verdadeira então verifica condição do solo
    @Rule(Fact(IrrigacaoBaixa=True), Fact(UmidadeSoloAcima60=True),
          Fact(PlantaAcima6=False))
    def SoloUmidoBaixa(self):
        self.declare(Fact(IrrigacaoBaixaFinal=False))
        print("Solo Muito umido - Não irrigar")

    # Regra 15
    @Rule(Fact(IrrigacaoBaixa=True), Fact(UmidadeSoloAbaixo60=True),
          Fact(PlantaAcima6=False))
    def SoloSecoBaixa(self):
        self.declare(Fact(IrrigacaoBaixaFinal=True))
        print("Ligar irrigação com frequencia diminuida pela metade!")

    # Regra 16
    # Se a planta tiver 6 metros ou mais a irrigação será cortada pela metade
    @Rule(Fact(TemperaturaAcima30=True), Fact(TempChuva=False),
          Fact(PlantaAcima6=True))
    def climaQuente(self):
        self.declare(Fact(IrrigacaoClimaQuente=True))
        print("Temperatura alta - Irigação será ligada de 2 em 2 horas com metade do volume de agua!")

    # Regra 17
    @Rule(Fact(TemperaturaAcima30=True), Fact(UmidadeArAbaixo30=True),
          Fact(TempChuva=False), Fact(PlantaAcima6=True))
    def superAquecido(self):
        self.declare(Fact(IrrigacaoDobrada=True))
        print("Ambiente superAquecido-Irrigação será ligada de 1 em 1 hora com metade do volume de agua!")

    # Regra 18
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeArAbaixo50=True),
          Fact(TempChuva=False), Fact(PlantaAcima6=True))
    def TempoSeco(self):
        self.declare(Fact(IrrigacaoNormalM=True))

    # Regra 19
    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeAr=True),
          Fact(TempChuva=False), Fact(PlantaAcima6=True))
    def TempoSeco(self):
        self.declare(Fact(IrrigacaoBaixaM=True))

    # Regra 20
    @Rule(Fact(TemperaturaMinima=True), Fact(TempChuva=False),
          Fact(PlantaAcima6=True))
    def TempoFrio(self):
        self.declare(Fact(IrrigacaoFrio=True))
        print("Clima muito frio - Não irrigar")

    # Regra 21
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeArAbaixo50=True),
           Fact(TempChuva=False), Fact(PlantaAcima6=True))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManhaM=True))

    # Regra 22
    @ Rule(Fact(Temperatura10_20=True), Fact(UmidadeAr=True),
           Fact(TempChuva=False), Fact(PlantaAcima6=True))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManhaM=False))
        print("Temperatura baixa - Não será ligada a irrigação!")

    # Regra 23
    @Rule(Fact(IrrigacaoNormalM=True), Fact(UmidadeSoloAcima60=True),
          Fact(PlantaAcima6=True))
    def SoloUmido(self):
        self.declare(Fact(IrrigacaoNormalFinalM=False))
        print("Solo Muito umido - Não irrigar")

    # Regra 24
    @Rule(Fact(IrrigacaoNormalM=True), Fact(UmidadeSoloAbaixo60=True),
          Fact(PlantaAcima6=True))
    def SoloSeco(self):
        self.declare(Fact(IrrigacaoNormalFinalM=True))
        print("Solo seco - Ligar irrigação com metade do volume de agua")

    # Regra 25
    @Rule(Fact(IrrigacaoManhaM=True), Fact(UmidadeSoloAcima60=True),
          Fact(PlantaAcima6=True))
    def SoloUmidoManha(self):
        self.declare(Fact(IrrigacaoManhaFinalM=False))
        print("Solo Muito umido - Não irrigar")

    # Regra 26
    @Rule(Fact(IrrigacaoManhaM=True), Fact(UmidadeSoloAbaixo60=True),
          Fact(PlantaAcima6=True))
    def SoloSecoManha(self):
        self.declare(Fact(IrrigacaoManhaFinalM=True))
        print("Ligar irrigação só uma vez de manhã com metade do volume de agua")

    # Regra 27
    @Rule(Fact(IrrigacaoBaixaM=True), Fact(UmidadeSoloAcima60=True),
          Fact(PlantaAcima6=True))
    def SoloUmidoBaixa(self):
        self.declare(Fact(IrrigacaoBaixaFinalM=False))
        print("Solo Muito umido - Não irrigar")

    # Regra 28
    @Rule(Fact(IrrigacaoBaixaM=True), Fact(UmidadeSoloAbaixo60=True),
          Fact(PlantaAcima6=True))
    def SoloSecoBaixa(self):
        self.declare(Fact(IrrigacaoBaixaFinalM=True))
        print("Ligar irrigação com frequencia diminuida pela metade e metade do volume de agua!")


engine = InferenceEngine()


engine.declare(Fact(TemperaturaAcima30=func.temperaturaAcima30(temp),
                    Temperatura20_30=func.temperatura20_30(temp),
                    UmidadeArAbaixo50=func.umidadeArAbaixo50(umidadeAr),
                    UmidadeArAbaixo30=func.umidadeArAbaixo30(umidadeAr),
                    UmidadeAr=func.umidadeAr50(umidadeAr),
                    TemperaturaMinima=func.temperaturaMinima(temp),
                    TempChuva=func.tempChuva(condClima),
                    UmidadeSoloAcima60=False,
                    UmidadeSoloAbaixo60=True,
                    PlantaAcima6=True
                    ))

# Altura da planta

# Quantidade de sol diaria (em horas)

engine.run()
engine.reset()
