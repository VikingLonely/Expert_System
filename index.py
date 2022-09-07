import sys
from experta import *


class my_Fact(Fact):

    pass


class InferenceEngine(KnowledgeEngine):
    @Rule(Fact(TemperaturaAcima30=True))
    def superAquecido(self):
        self.declare(Fact(Irrigacao=True))
        print("Irrigação Ligada")

    @Rule(Fact(Temperatura20_30=True), Fact(UmidadeAr=P(lambda x: x <= 50)))
    def TempoSeco(self):
        self.declare(Fact(Irrigacao=True))
        print("irrigacao Ligada")

    @Rule(Fact(TemperaturaMinima=True))
    def TempoFrio(self):
        self.declare(Fact(Irrigacao=False))
        print("Não irrigar")

    @ Rule(Fact(Temperatura10_20=True))
    def Manhã(self):
        self.declare(Fact(IrrigacaoManha=True))
        print("Irrigar só de manhã")


engine = InferenceEngine()
engine.reset()

engine.declare(Fact(TemperaturaAcima30=False,
                    Temperatura20_30=False,
                    UmidadeAr=25,
                    TemperaturaMinima=True))

engine.run()
