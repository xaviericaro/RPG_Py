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
        self.pontos_disponiveis = 0
        
        self.inventario = []
        self.arma = None
        self.armadura = None

        self.defendendo = False
        self.ouro = 0

        self.quests = {}

    # =========================
    # COMBATE
    # =========================
    def ataque_total(self):
        bonus = self.arma.get("ataque", 0) if self.arma else 0
        return self.ataque + bonus

    def defesa_total(self):
        bonus = self.armadura.get("defesa", 0) if self.armadura else 0
        total = self.defesa + bonus
        return total * 2 if self.defendendo else total

    def ataque_normal(self, alvo):
        dano_bruto = random.randint(
            self.ataque_total() - 3,
            self.ataque_total() + 3,
        )

        dano_final = max(0, dano_bruto - alvo.defesa_total())
        alvo.vida = max(0, alvo.vida - dano_final)

        print(f"🗡️ {self.nome} causou {dano_final} de dano!")

    def aplicar_status(self):
        for efeito in list(self.status):
            self.status[efeito] -= 1

            if efeito == "veneno":
                self.vida = max(0, self.vida - 3)
                print(f"☠️ {self.nome} sofreu 3 de dano por veneno!")

            elif efeito == "sangramento":
                self.vida = max(0, self.vida - 5)
                print(f"🩸 {self.nome} sangra e perde 5 de vida!")

            if self.status[efeito] <= 0:
                del self.status[efeito]

    # =========================
    # EQUIPAMENTOS
    # =========================
    def equipar_arma(self, arma):
        self.arma = arma
        print(f"⚔️ {arma['nome']} equipada! (+{arma.get('ataque', 0)} ATK)")

    def equipar_armadura(self, armadura):
        self.armadura = armadura
        print(f"🛡️ {armadura['nome']} equipada! (+{armadura.get('defesa', 0)} DEF)")

    # =========================
    # QUESTS
    # =========================
    def mostrar_quests(self):
        quests_ativas = [
            q for q in self.quests.values()
            if q.aceita
        ]

        if not quests_ativas:
            print("📭 Você não possui quests ativas.")
            return

        print("\n📜 DIÁRIO DE QUESTS")
        for quest in quests_ativas:
            if quest.entregue:
                status = "🔵 Entregue"
            elif quest.concluida:
                status = "🟢 Concluída"
            else:
                status = "🟡 Em progresso"

            print(
                f"\n[{quest.id}]"
                f"\n{quest.descricao}"
                f"\nStatus: {status}"
                f"\nProgresso: {quest.progresso}/{quest.quantidade}"
                f"\nRecompensa: {quest.recompensa_ouro} ouro"
            )

    # =========================
    # XP / LEVEL
    # =========================
    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        print(f"⭐ {self.nome} ganhou {quantidade} XP!")

        while self.xp >= self.xp_para_proximo:
            self.xp -= self.xp_para_proximo
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp_para_proximo = int(self.xp_para_proximo * 1.5)

        self.pontos_disponiveis += 5

        self.vida_max += 10
        self.ataque += 2
        self.defesa += 2
        self.mana_max += 5

        self.vida = self.vida_max
        self.mana = self.mana_max

        print(f"\n✨ NÍVEL UP! Você agora está no nível {self.nivel}!")
        print(f"🎁 Você ganhou 5 pontos de atributo! Total: {self.pontos_disponiveis}")
    # =========================
    # UTIL
    # =========================
    def esta_vivo(self):
        return self.vida > 0
