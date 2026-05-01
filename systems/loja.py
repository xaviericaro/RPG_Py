# systems/loja.py

def loja(jogador):
    itens_loja = [
        {"nome": "Poção de Cura", "tipo": "consumivel", "cura": 30, "preco": 15},
        {"nome": "Poção Grande", "tipo": "consumivel", "cura": 60, "preco": 30},
        {"nome": "Espada de Ferro", "tipo": "arma", "ataque": 6, "preco": 50},
        {"nome": "Armadura de Couro", "tipo": "armadura", "defesa": 4, "preco": 40},
    ]

    while True:
        print("\n🏪 LOJA")
        print(f"🪙 Ouro: {jogador.ouro}")
        print("1 - Comprar")
        print("2 - Vender")
        print("0 - Sair")

        escolha = input(">>> ")

        if escolha == "1":
            comprar(jogador, itens_loja)
        elif escolha == "2":
            vender(jogador)
        elif escolha == "0":
            break
        else:
            print("❌ Opção inválida.")

def comprar(jogador, itens_loja):
    print("\n🛒 ITENS À VENDA")

    for i, item in enumerate(itens_loja):
        print(f"{i+1} - {item['nome']} ({item['preco']} ouro)")

    print("0 - Cancelar")
    escolha = input(">>> ")

    if not escolha.isdigit():
        return

    escolha = int(escolha)

    if escolha == 0:
        return

    if escolha < 1 or escolha > len(itens_loja):
        print("❌ Escolha inválida.")
        return

    item = itens_loja[escolha - 1]

    if jogador.ouro < item["preco"]:
        print("❌ Ouro insuficiente.")
        return

    jogador.ouro -= item["preco"]
    jogador.inventario.append(item.copy())

    print(f"✅ Você comprou {item['nome']}!")

def vender(jogador):
    if not jogador.inventario:
        print("📦 Seu inventário está vazio.")
        return

    print("\n📤 VENDER ITENS")

    for i, item in enumerate(jogador.inventario):
        preco = item.get("preco", 5)
        print(f"{i+1} - {item['nome']} (vende por {preco} ouro)")

    print("0 - Cancelar")
    escolha = input(">>> ")

    if not escolha.isdigit():
        return

    escolha = int(escolha)

    if escolha == 0:
        return

    if escolha < 1 or escolha > len(jogador.inventario):
        print("❌ Escolha inválida.")
        return

    item = jogador.inventario.pop(escolha - 1)
    preco = item.get("preco", 5)

    if jogador.arma == item:
        jogador.arma = None
    if jogador.armadura == item:
        jogador.armadura = None

    jogador.ouro += preco
    print(f"💰 Você vendeu {item['nome']} por {preco} ouro.")