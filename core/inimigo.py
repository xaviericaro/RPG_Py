import random


class Inimigo:
    def __init__(
        self,
        nome,
        vida,
        ataque,
        defesa,
        xp_drop,
        ouro_drop,
    ):
        self.nome = nome

        self.vida_max = vida
        self.vida = self.vida_max

        self.ataque = ataque
        self.defesa = defesa

        self.xp_drop = xp_drop
        self.ouro_drop = ouro_drop

        self.status = {}
        self.defendendo = False

    # ======================
    # COMBATE
    # ======================
    def ataque_total(self):
        return self.ataque

    def defesa_total(self):
        total = self.defesa
        return total * 2 if self.defendendo else total

    def atacar(self, alvo):
        dano = max(
            0,
            random.randint(self.ataque_total() - 2, self.ataque_total() + 2)
            - alvo.defesa_total()
        )
        alvo.vida = max(0, alvo.vida - dano)
        print(f"{self.nome} atacou e causou {dano} de dano!")

    # ======================
    # STATUS
    # ======================
    def aplicar_status(self):
        for efeito in list(self.status):
            self.status[efeito] -= 1

            if efeito == "veneno":
                self.vida -= 3
                print(f"☠️ {self.nome} sofreu 3 de dano por veneno!")

            if efeito == "sangramento":
                self.vida -= 5
                print(f"🩸 {self.nome} sangra e perde 5 de vida!")

            if self.status[efeito] <= 0:
                del self.status[efeito]

    # ======================
    # UTILIDADES
    # ======================
    def esta_vivo(self):
        return self.vida > 0
