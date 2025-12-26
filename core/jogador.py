import random
from core.personagem import Personagem


class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=120,
            ataque=15,
            defesa=10,
            mana=30,
        )

    def habilidade(self, alvo):
        custo = 10
        if self.mana < custo:
            print("❌ Mana insuficiente!")
            return

        self.mana -= custo

        dano = random.randint(20, 30)
        dano_final = max(0, dano - alvo.defesa_total())
        alvo.vida = max(0, alvo.vida - dano_final)

        alvo.status["sangramento"] = 2
        print(f"💥 Golpe Brutal causou {dano_final} de dano!")


class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=80,
            ataque=10,
            defesa=5,
            mana=60,
        )

    def habilidade(self, alvo):
        custo = 15
        if self.mana < custo:
            print("❌ Mana insuficiente!")
            return

        self.mana -= custo

        dano = random.randint(25, 40)
        dano_final = max(0, dano - alvo.defesa_total())
        alvo.vida = max(0, alvo.vida - dano_final)

        alvo.status["veneno"] = 3
        print(f"🔥 Bola de Fogo causou {dano_final} de dano!")


class Arqueiro(Personagem):
    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=100,
            ataque=13,
            defesa=7,
            mana=40,
        )

    def habilidade(self, alvo):
        custo = 12
        if self.mana < custo:
            print("❌ Mana insuficiente!")
            return

        self.mana -= custo

        dano = random.randint(18, 28)
        dano_final = max(0, dano - alvo.defesa_total())
        alvo.vida = max(0, alvo.vida - dano_final)

        if random.random() < 0.4:
            alvo.status["sangramento"] = 3
            print("🩸 O inimigo começou a sangrar!")

        print(f"🏹 Tiro Preciso causou {dano_final} de dano!")
