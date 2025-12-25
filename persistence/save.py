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
        "classe": jogador.__class__.__name__,
        "dados": jogador.__dict__,
        "area": area
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

    jogador = classes[dados["classe"]](dados["dados"]["nome"])
    jogador.__dict__.update(dados["dados"])
    return jogador, dados["area"]