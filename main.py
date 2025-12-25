import os
from core.jogador import Guerreiro, Mago, Arqueiro
from persistence.save import definir_save, carregar_jogo, salvar_jogo
from systems.mapa import loop_mapa

print("=== RPG EM PYTHON ===")
print("1 - Continuar jogo")
print("2 - Novo jogo")
opcao = input(">>> ")

print("\nEscolha o slot:")
print("1 - Slot 1")
print("2 - Slot 2")
print("3 - Slot 3")
slot = input(">>> ")

save_path = f"saves/save_slot_{slot}.json"
definir_save(save_path)

# =========================
# CONTINUAR JOGO
# =========================
if opcao == "1" and os.path.exists(save_path):
    jogador, area_atual = carregar_jogo()
    print(f"\n🔄 Bem-vindo de volta, {jogador.nome}!")
    print(f"📍 Última localização: {area_atual}")

# =========================
# NOVO JOGO
# =========================
else:
    print("\n=== CRIAÇÃO DE PERSONAGEM ===")
    nome = input("Digite o nome do personagem: ")

    print("\nEscolha sua classe:")
    print("1 - Guerreiro")
    print("2 - Mago")
    print("3 - Arqueiro")
    classe = input(">>> ")

    if classe == "1":
        jogador = Guerreiro(nome)
    elif classe == "2":
        jogador = Mago(nome)
    elif classe == "3":
        jogador = Arqueiro(nome)
    else:
        print("Classe inválida!")
        exit()

    jogador.inventario = [
        {"nome": "Poção de Cura", "tipo": "consumivel", "cura": 30},
        {"nome": "Espada Enferrujada", "tipo": "arma", "ataque": 3},
    ]

    area_atual = "Vilarejo"
    salvar_jogo(jogador, area_atual)

# =========================
# INICIAR MAPA
# =========================
loop_mapa(jogador, area_atual)