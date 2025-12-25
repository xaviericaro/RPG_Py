def loja(jogador):
    itens = [
        {"nome": "Poção de Cura", "tipo": "consumivel", "cura": 30, "preco": 20},
        {"nome": "Poção Grande", "tipo": "consumivel", "cura": 60, "preco": 50},
        {"nome": "Espada de Ferro", "tipo": "arma", "ataque": 6, "preco": 100},
        {"nome": "Armadura de Couro", "tipo": "armadura", "defesa": 4, "preco": 80},
    ]

    while True:
        print("\n🏪 LOJA")
        print(f"💰 Ouro: {jogador.ouro}")

        for i, item in enumerate(itens):
            print(f"{i+1} - {item['nome']} ({item['preco']} ouro)")

        print("0 - Sair")
        escolha = input(">>> ")

        if escolha == "0":
            return

        escolha = int(escolha) - 1
        if escolha < 0 or escolha >= len(itens):
            continue

        item = itens[escolha]

        if jogador.ouro < item["preco"]:
            print("❌ Ouro insuficiente!")
            continue

        jogador.ouro -= item["preco"]
        jogador.inventario.append(item.copy())
        print(f"✅ Você comprou {item['nome']}!")
