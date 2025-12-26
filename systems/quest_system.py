import json
import os

QUESTS_FILE = "data/quests.json"


class Quest:
    def __init__(
        self,
        quest_id,
        descricao,
        tipo_evento,
        area_objetivo,
        quantidade,
        recompensa_ouro,
        dialogos
    ):
        self.id = quest_id
        self.descricao = descricao
        self.tipo_evento = tipo_evento
        self.area_objetivo = area_objetivo
        self.quantidade = quantidade
        self.recompensa_ouro = recompensa_ouro
        self.dialogos = dialogos  # Armazena as falas do JSON

        self.progresso = 0
        self.aceita = False
        self.concluida = False
        self.entregue = False

    # =========================
    # EVENTOS
    # =========================
    def registrar_evento(self, area):
        if not self.aceita or self.concluida:
            return

        if area != self.area_objetivo:
            return

        self.progresso += 1
        print(
            f"📜 Quest '{self.id}': {self.progresso}/{self.quantidade}"
        )

        if self.progresso >= self.quantidade:
            self.concluida = True
            print(f"✅ Quest '{self.id}' concluída! Volte ao NPC.")

    # =========================
    # ENTREGA
    # =========================
    def entregar(self, jogador):
        if not self.concluida or self.entregue:
            return False

        jogador.ouro += self.recompensa_ouro
        self.entregue = True

        print(f"🪙 Você recebeu {self.recompensa_ouro} de ouro!")
        return True


# =========================
# CARREGAR QUESTS
# =========================
def carregar_quests():
    quests = {}

    if not os.path.exists(QUESTS_FILE):
        return quests

    with open(QUESTS_FILE, encoding="utf-8") as f:
        dados = json.load(f)

    for quest_id, q in dados.items():
        quests[quest_id] = Quest(
            quest_id=quest_id,
            descricao=q["descricao"],
            tipo_evento=q.get("tipo_evento", "geral"),
            area_objetivo=q["area_objetivo"],
            quantidade=q["quantidade"],
            recompensa_ouro=q["recompensa_ouro"],
            dialogos=q.get("dialogos", {}) # <--- Carrega do JSON
        )
    return quests