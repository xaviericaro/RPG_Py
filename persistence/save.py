import json
import os
from core.jogador import Guerreiro, Mago, Arqueiro

SAVE_FILE = None

def definir_save(path):
    global SAVE_FILE
    SAVE_FILE = path
    os.makedirs("saves", exist_ok=True)

def salvar_jogo(jogador, area):
    dados = {
    "nome": jogador.nome,
    "classe": jogador.__class__.__name__,
    "nivel": jogador.nivel,
    "xp": jogador.xp,
    "vida": jogador.vida,
    "vida_max": jogador.vida_max,
    "mana": jogador.mana,
    "mana_max": jogador.mana_max,
    "status": jogador.status,
    "inventario": jogador.inventario,
    "ouro": jogador.ouro,
    "quests": {
    qid: {
        "progresso": q.progresso,
        "aceita": q.aceita,
        "concluida": q.concluida,
        "entregue": q.entregue
    } for qid, q in jogador.quests.items()
}

}
    
    with open(SAVE_FILE, "w") as f:
        json.dump(dados, f, indent=4)


def carregar_jogo():
    with open(SAVE_FILE) as f:
        dados = json.load(f)

    classes = {
        "Guerreiro": Guerreiro,
        "Mago": Mago,
        "Arqueiro": Arqueiro,
    }

    # cria jogador pela classe
    jogador = classes[dados["classe"]](dados["nome"])

    # restaura atributos básicos
    jogador.nivel = dados["nivel"]
    jogador.xp = dados["xp"]
    jogador.vida_max = dados.get("vida_max", jogador.vida_max)
    jogador.vida = min(dados["vida"], jogador.vida_max)

    jogador.ouro = dados["ouro"]
    jogador.inventario = dados["inventario"]

    # quests
    jogador.quests = {}

    if "quests" in dados:
        from systems.npc import Quest

        for qid, qdados in dados["quests"].items():
            if qid == "limpar_floresta":
                quest = Quest(
                    quest_id="limpar_floresta",
                    descricao="Derrote 2 inimigos na Floresta e volte até mim.",
                    area_objetivo="Floresta",
                    quantidade=2,
                    recompensa_ouro=50,
                )

                quest.progresso = qdados.get("progresso", 0)
                quest.aceita = qdados.get("aceita", False)
                quest.concluida = qdados.get("concluida", False)
                quest.entregue = qdados.get("entregue", False)

                jogador.quests[qid] = quest

    area_atual = dados.get("area", "Vilarejo")
    return jogador, area_atual