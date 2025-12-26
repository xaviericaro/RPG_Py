import time


def escrever(texto, delay=0.02):
    for c in texto:
        print(c, end="", flush=True)
        time.sleep(delay)
    print("\n")


# =========================
# INTRODUÇÃO
# =========================
def introducao():
    escrever(
        "Em um mundo ameaçado por forças antigas,\n"
        "criaturas emergem das sombras.\n"
    )
    escrever(
        "Poucos têm coragem de enfrentá-las.\n"
        "Hoje, um novo herói surge.\n"
    )


# =========================
# EVENTOS DE HISTÓRIA
# =========================
def encontro_goblin():
    escrever("Um Goblin salta das sombras, brandindo uma adaga enferrujada!")


def encontro_orc():
    escrever("O chão treme.\nUm Orc Brutal bloqueia seu caminho!")


def encontro_lobo():
    escrever("Olhos brilhantes surgem entre as árvores.\nUm Lobo Sombrio ataca!")


def chegada_montanha():
    escrever(
        "O ar fica pesado.\n"
        "Um rugido ecoa pelos céus.\n"
        "O Dragão Ancião sabe que você chegou.\n"
    )


def final_vitoria():
    escrever(
        "Com o último golpe, o Dragão cai.\n"
        "A paz retorna ao mundo.\n"
        "Seu nome será lembrado.\n"
        "FIM.\n"
    )


def final_derrota():
    escrever(
        "Você caiu.\n"
        "O mundo permanece em trevas.\n"
        "FIM.\n"
    )
