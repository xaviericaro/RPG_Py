def usar_item(jogador):
    if not jogador.inventario:
        print("🎒 Inventário vazio.")
        return

    print("\n🎒 SEU INVENTÁRIO (Agrupado):")
    contagem = {}
    indices_originais = {} 

    for i, item in enumerate(jogador.inventario):
        nome = item["nome"]
        if nome not in contagem:
            contagem[nome] = 0
            indices_originais[nome] = i
        contagem[nome] += 1

    lista_menu = list(contagem.keys())
    for i, nome in enumerate(lista_menu, start=1):
        print(f"{i} - {nome} (x{contagem[nome]})")

    entrada = input("\nEscolha um item para interagir (ou 0 para voltar): ")
    if not entrada.isdigit(): return
    escolha = int(entrada)
    if escolha == 0: return

    nome_item = lista_menu[escolha - 1]
    indice_real = indices_originais[nome_item]
    item = jogador.inventario.pop(indice_real) # Removemos para equipar ou usar

    if item["tipo"] == "consumivel":
        cura = item.get("cura", 0)
        jogador.vida = min(jogador.vida + cura, jogador.vida_max)
        print(f"🧪 Você usou {item['nome']} e recuperou {cura} HP.")

    elif item["tipo"] == "arma":
        jogador.equipar_arma(item)

    elif item["tipo"] == "armadura":
        jogador.equipar_armadura(item)

    elif item["tipo"] == "material":
        print(f"📦 {item['nome']} é material. Vá ao Ferreiro!")
        jogador.inventario.append(item) # Devolve pois material não se "usa" aqui