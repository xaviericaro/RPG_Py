import json
import os
import re 

from core.jogador import Guerreiro, Mago, Arqueiro

SAVE_FILE = None

# =========================
# DEFINIR SLOT DE SAVE
# =========================
def definir_save(caminho):
    global SAVE_FILE
    
    caminho_limpo = re.sub(r'[&<>|]', '', caminho)
    
    if not caminho_limpo.startswith("saves"):
        caminho_limpo = os.path.join("saves", os.path.basename(caminho_limpo))
    
    SAVE_FILE = caminho_limpo

    pasta = os.path.dirname(SAVE_FILE)
    if pasta and not os.path.exists(pasta):
        try:
            os.makedirs(pasta, exist_ok=True)
        except OSError:
            SAVE_FILE = os.path.basename(SAVE_FILE)



# =========================
# SALVAR JOGO
# =========================
def salvar_jogo(jogador, area_atual):
    if not SAVE_FILE:
        return

    dados = {
        "classe": jogador.__class__.__name__,
        "area": area_atual,
        "jogador": {
            "nome": jogador.nome,
            "nivel": jogador.nivel,
            "pontos_disponiveis": jogador.pontos_disponiveis,
            "xp": jogador.xp,
            "xp_para_proximo": jogador.xp_para_proximo,
            "vida": jogador.vida,
            "vida_max": jogador.vida_max,
            "mana": jogador.mana,
            "mana_max": jogador.mana_max,
            "ataque": jogador.ataque,
            "defesa": jogador.defesa,
            "ouro": jogador.ouro,
            "inventario": jogador.inventario,
            "arma": jogador.arma,
            "armadura": jogador.armadura,
        },
        "quests": {},
    }

    # salvar estado das quests
    for qid, quest in jogador.quests.items():
        dados["quests"][qid] = {
            "progresso": quest.progresso,
            "concluida": quest.concluida,
            "entregue": getattr(quest, "entregue", False),
        }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print("💾 Jogo salvo com sucesso!")


# =========================
# CARREGAR JOGO
# =========================
def carregar_jogo():
    if not SAVE_FILE or not os.path.exists(SAVE_FILE):
        raise FileNotFoundError("Save não encontrado.")

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)

    dados_quests_salvas = dados.get("quests", {})

    classes = {
        "Guerreiro": Guerreiro,
        "Mago": Mago,
        "Arqueiro": Arqueiro,
    }

    classe = dados["classe"]
    info = dados["jogador"]

    jogador = classes[classe](info["nome"])

    # restaurar atributos básicos
    jogador.nivel = info["nivel"]
    jogador.pontos_disponiveis = info.get("pontos_disponiveis", 0)
    jogador.xp = info["xp"]
    jogador.xp_para_proximo = info["xp_para_proximo"]

    jogador.vida_max = info["vida_max"]
    jogador.vida = min(info["vida"], jogador.vida_max)

    jogador.mana_max = info["mana_max"]
    jogador.mana = min(info["mana"], jogador.mana_max)

    jogador.ataque = info["ataque"]
    jogador.defesa = info["defesa"]

    jogador.ouro = info["ouro"]
    jogador.inventario = info["inventario"]
    jogador.arma = info["arma"]
    jogador.armadura = info["armadura"]

    # quests serão recriadas fora (quest_system)
    jogador.quests = {}

    area_atual = dados.get("area", "Vilarejo")

    return jogador, area_atual, dados_quests_salvas