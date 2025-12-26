import random

class Personagem:
    def __init__(self, nome, vida, ataque, defesa, mana=0):
        self.nome = nome

        self.vida_max = vida
        self.vida = self.vida_max

        self.ataque = ataque
        self.defesa = defesa

        self.mana_max = mana
        self.mana = self.mana_max

        self.status = {}

        self.nivel = 1
        self.xp = 0
        self.xp_para_proximo = 100

        self.inventario = []
        self.arma = None
        self.armadura = None

        self.defendendo = False
        self.status = {}

        self.ouro = 0

        self.quests = {}

    def ataque_total(self):
        bonus = self.arma["ataque"] if self.arma else 0
        return self.ataque + bonus

    def defesa_total(self):
        bonus = self.armadura["defesa"] if self.armadura else 0
        total = self.defesa + bonus
        return total * 2 if self.defendendo else total

    def ataque_normal(self, alvo):
        dano = max(
            0,
            random.randint(self.ataque_total() - 3, self.ataque_total() + 3)
            - alvo.defesa_total()
        )
        alvo.vida -= dano
        print(f"{self.nome} atacou e causou {dano} de dano!")

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


    def mostrar_quests(self):
        if not self.quests:
            print("📭 Você não possui quests ativas.")
            return

        print("\n📜 DIÁRIO DE QUESTS")
        for quest in self.quests.values():
            status = "🟢 Concluída" if quest.concluida else "🟡 Em progresso"
            if quest.entregue:
                status = "🔵 Entregue"

            print(f"""
    [{quest.id}]
    {quest.descricao}
    Status: {status}
    Progresso: {quest.progresso}/{quest.quantidade}
    Recompensa: {quest.recompensa_ouro} ouro
    """)


    def esta_vivo(self):
        return self.vida > 0

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        print(f"⭐ {self.nome} ganhou {quantidade} XP!")

        while self.xp >= self.xp_para_proximo:
            self.xp -= self.xp_para_proximo
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp_para_proximo = int(self.xp_para_proximo * 1.5)

        self.vida_max += 10
        self.ataque += 2
        self.defesa += 2
        self.mana_max += 5

        self.vida = self.vida_max
        self.mana = self.mana_max

        print(f"\n⬆️ {self.nome} subiu para o nível {self.nivel}!")
        print("❤️ Vida +10 | ⚔️ Ataque +2 | 🛡️ Defesa +2 | 🔮 Mana +5\n")
