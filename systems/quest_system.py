import json


class Quest:
    def __init__(self, quest_id, dados):
        self.id = quest_id
        self.descricao = dados["descricao"]
        self.area_objetivo = dados["area_objetivo"]
        self.quantidade = dados["quantidade"]
        self.recompensa_ouro = dados["recompensa_ouro"]

        self.progresso = dados.get("progresso", 0)
        self.aceita = dados.get("aceita", False)
        self.concluida = dados.get("concluida", False)
        self.entregue = dados.get("entregue", False)

    def registrar_evento(self, area):
        if not self.aceita or self.concluida or self.entregue:
            return

        if area == self.area_objetivo:
            self.progresso += 1
            print(f"📜 Quest {self.id}: {self.progresso}/{self.quantidade}")

            if self.progresso >= self.quantidade:
                self.concluida = True
                print("✅ Quest concluída! Volte ao NPC.")


def carregar_quests():
    with open("data/quests.json", encoding="utf-8") as f:
        dados = json.load(f)

    quests = {}
    for quest_id, quest_dados in dados.items():
        quests[quest_id] = Quest(quest_id, quest_dados)

    return quests
