import random
from core.personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, nome, vida, ataque, defesa, xp, ouro):
        super().__init__(nome, vida, ataque, defesa)
        self.xp_drop = xp
        self.ouro_drop = ouro

    def atacar(self, alvo):
        dano = max(
            0,
            random.randint(self.ataque - 2, self.ataque + 4)
            - alvo.defesa_total()
        )
        alvo.vida -= dano
        print(f"{self.nome} atacou causando {dano}!")
