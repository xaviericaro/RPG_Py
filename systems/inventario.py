def usar_item(jogador):
    if not jogador.inventario:
        print("🎒 Inventário vazio.")
        return

    print("\n🎒 Inventário:")
    for i, item in enumerate(jogador.inventario, start=1):
        print(f"{i} - {item['nome']}")

    entrada = input("Escolha um item ou 0 para voltar: ")

    if not entrada.isdigit():
        print("❌ Entrada inválida.")
        return

    escolha = int(entrada)

    if escolha == 0:
        return

    if escolha < 1 or escolha > len(jogador.inventario):
        print("❌ Item inválido.")
        return

    item = jogador.inventario[escolha - 1]

    # =========================
    # CONSUMÍVEL
    # =========================
    if item["tipo"] == "consumivel":
        cura = item.get("cura", 0)
        jogador.vida = min(jogador.vida + cura, jogador.vida_max)
        print(f"🧪 Você usou {item['nome']} e recuperou {cura} HP.")
        jogador.inventario.pop(escolha - 1)

    # =========================
    # ARMA
    # =========================
    elif item["tipo"] == "arma":
        jogador.equipar_arma(item)
        jogador.inventario.pop(escolha - 1)

    else:
        print("❌ Tipo de item desconhecido.")
