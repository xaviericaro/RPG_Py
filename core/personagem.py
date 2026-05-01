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
        
        # Slots de Equipamento
        self.arma = None
        self.armadura = None

        self.defendendo = False
        self.ouro = 0
        self.quests = {}

    # COMBATE
    def ataque_total(self):
        # Soma ataque base + ataque da arma equipada
        bonus = self.arma.get("ataque", 0) if self.arma else 0
        return self.ataque + bonus

    def defesa_total(self):
        # Soma defesa base + defesa da armadura equipada
        bonus = self.armadura.get("defesa", 0) if self.armadura else 0
        total = self.defesa + bonus
        return total * 2 if self.defendendo else total

    def ataque_normal(self, alvo):
        dano_bruto = random.randint(self.ataque_total() - 3, self.ataque_total() + 3)
        dano_final = max(0, dano_bruto - alvo.defesa_total())
        alvo.vida = max(0, alvo.vida - dano_final)
        print(f"🗡️ {self.nome} causou {dano_final} de dano!")


    # EQUIPAMENTOS 
    def equipar_arma(self, nova_arma):
        if "durabilidade" not in nova_arma:
            nova_arma["durabilidade"] = 100 
            
        if self.arma:
            self.inventario.append(self.arma)
        
        self.arma = nova_arma
        print(f"⚔️ {nova_arma['nome']} equipada! Durabilidade: {nova_arma['durabilidade']}%")

    def usar_durabilidade(self):
        """Chame isso após cada ataque ou defesa no systems/batalha.py"""
        if self.arma:
            self.arma["durabilidade"] -= 2
            if self.arma["durabilidade"] <= 0:
                self.arma["durabilidade"] = 0
                print(f"⚠️ Sua {self.arma['nome']} está quebrada e perdeu a eficiência!")
    def equipar_armadura(self, nova_armadura):
        if self.armadura:
            self.inventario.append(self.armadura) # Devolve a antiga
            print(f"📦 {self.armadura['nome']} voltou para o inventário.")
            
        self.armadura = nova_armadura
        print(f"🛡️ {nova_armadura['nome']} equipada! (+{nova_armadura.get('defesa', 0)} DEF)")

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

    def esta_vivo(self):
        return self.vida > 0
    
    def reduzir_durabilidade_equipamentos(self):
        """Reduz a durabilidade da arma e armadura após cada ação de combate."""
        if self.arma and "durabilidade" in self.arma:
            self.arma["durabilidade"] -= 1  # Perde 1% por ataque
            if self.arma["durabilidade"] < 0: self.arma["durabilidade"] = 0
            
        if self.armadura and "durabilidade" in self.armadura:
            self.armadura["durabilidade"] -= 1 # Perde 1% ao ser atingido
            if self.armadura["durabilidade"] < 0: self.armadura["durabilidade"] = 0