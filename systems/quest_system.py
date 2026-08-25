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
        dialogos,
        alvo=None,
        recompensa_xp=0,
        recompensa_item=None,
    ):
        self.id = quest_id
        self.descricao = descricao
        self.tipo_evento = tipo_evento          # matar_area | matar_alvo | entregar_item | coletar_item
        self.area_objetivo = area_objetivo
        self.quantidade = quantidade
        self.recompensa_ouro = recompensa_ouro
        self.recompensa_xp = recompensa_xp
        self.recompensa_item = recompensa_item  # nome de um item em data.database.ITENS (opcional)
        self.dialogos = dialogos
        self.alvo = alvo                        # nome do inimigo ou item, dependendo do tipo

        self.progresso = 0
        self.aceita = False
        self.concluida = False
        self.entregue = False

    # --- Eventos de combate (matar_area / matar_alvo) ---
    def registrar_evento(self, area=None, nome_inimigo=None):
        if not self.aceita or self.concluida:
            return

        avancou = False

        if self.tipo_evento == "matar_area" and area == self.area_objetivo:
            avancou = True
        elif self.tipo_evento == "matar_alvo" and nome_inimigo == self.alvo:
            avancou = True

        if not avancou:
            return

        self.progresso += 1
        print(f"📜 Quest '{self.id}': {self.progresso}/{self.quantidade}")

        if self.progresso >= self.quantidade:
            self.concluida = True
            print(f"✅ Quest '{self.id}' concluída! Volte ao NPC.")

    # --- Eventos de posse de item (entregar_item / coletar_item) ---
    def verificar_item(self, jogador):
        """Chamado ao falar com o NPC: verifica se o jogador já carrega os itens necessários."""
        if not self.aceita or self.concluida:
            return
        if self.tipo_evento not in ("entregar_item", "coletar_item"):
            return

        qtd = sum(1 for it in jogador.inventario if it.get("nome") == self.alvo)
        self.progresso = min(qtd, self.quantidade)

        if self.progresso >= self.quantidade:
            self.concluida = True

    def entregar(self, jogador):
        if not self.concluida or self.entregue:
            return False

        # Consome os itens de entrega, se aplicável
        if self.tipo_evento == "entregar_item":
            restantes = self.quantidade
            nova_lista = []
            for it in jogador.inventario:
                if restantes > 0 and it.get("nome") == self.alvo:
                    restantes -= 1
                    continue
                nova_lista.append(it)
            jogador.inventario = nova_lista

        if self.recompensa_ouro:
            jogador.ouro += self.recompensa_ouro
            print(f"🪙 Você recebeu {self.recompensa_ouro} de ouro!")

        if self.recompensa_xp:
            jogador.ganhar_xp(self.recompensa_xp)

        if self.recompensa_item:
            from data.database import ITENS
            if self.recompensa_item in ITENS:
                item = ITENS[self.recompensa_item].copy()
                item["nome"] = self.recompensa_item
                jogador.inventario.append(item)
                print(f"🎁 Você recebeu [{self.recompensa_item}]!")

        self.entregue = True
        return True


def carregar_quests():
    quests = {}

    if not os.path.exists(QUESTS_FILE):
        print(f"⚠️  Não encontrei o arquivo de missões em: {QUESTS_FILE}")
        print("   (o jogo vai continuar, mas nenhuma missão vai aparecer)")
        return quests


def aplicar_progresso_salvo(quests, dados_salvos):
    """Reaplica o estado (aceita/progresso/concluida/entregue) salvo no save às quests recarregadas.

    Sem isso, toda missão em andamento voltava para 'não aceita' ao carregar o jogo.
    """
    for quest_id, estado in (dados_salvos or {}).items():
        quest = quests.get(quest_id)
        if not quest:
            continue
        quest.aceita = estado.get("aceita", False)
        quest.progresso = estado.get("progresso", 0)
        quest.concluida = estado.get("concluida", False)
        quest.entregue = estado.get("entregue", False)
    return quests
