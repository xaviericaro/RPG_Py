import random
from core.personagem import Personagem

class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 120, 15, 10, 30)

    def habilidade(self, alvo):
        if self.mana < 10:
            print("Mana insuficiente!")
            return
        self.mana -= 10
        dano = random.randint(20, 30)
        alvo.vida -= dano
        alvo.status["sangramento"] = 2
        print(f"💥 Golpe Brutal causou {dano}!")


class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 80, 12, 5, 80)

    def habilidade(self, alvo):
        if self.mana < 15:
            print("Mana insuficiente!")
            return
        self.mana -= 15
        dano = random.randint(30, 45)
        alvo.vida -= dano
        alvo.status["veneno"] = 3
        print(f"🔥 Bola de Fogo causou {dano}!")


class Arqueiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, 100, 14, 8, 40)

    def habilidade(self, alvo):
        if self.mana < 8:
            print("Mana insuficiente!")
            return
        self.mana -= 8
        dano = random.randint(25, 35)
        alvo.vida -= dano
        print(f"🏹 Flecha Precisa causou {dano}!")
