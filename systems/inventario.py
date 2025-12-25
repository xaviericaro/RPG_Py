def usar_item(jogador):
    if not jogador.inventario:
        print("🎒 Inventário vazio!")
        return

    for i, item in enumerate(jogador.inventario):
        print(f"{i+1} - {item['nome']} ({item['tipo']})")

    escolha = int(input("Escolha o item: ")) - 1
    if escolha < 0 or escolha >= len(jogador.inventario):
        return

    item = jogador.inventario[escolha]

    if item["tipo"] == "consumivel":
        jogador.vida = min(jogador.vida_max, jogador.vida + item["cura"])
        jogador.inventario.pop(escolha)
        print(f"🧪 Você usou {item['nome']}")

    elif item["tipo"] == "arma":
        if jogador.arma:
            jogador.inventario.append(jogador.arma)
            print(f"🔁 {jogador.arma['nome']} voltou para o inventário.")

        jogador.arma = item
        jogador.inventario.pop(escolha)
        print(f"🗡️ {item['nome']} equipada! (+{item['ataque']} ATQ)")


    elif item["tipo"] == "armadura":
        jogador.armadura = item
        print(f"🛡️ {item['nome']} equipada!")
