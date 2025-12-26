from systems.inventario import usar_item


def batalha(jogador, inimigo):
    print(f"\n⚔️ Um {inimigo.nome} apareceu!")

    while jogador.esta_vivo() and inimigo.esta_vivo():
        jogador.aplicar_status()

        print(
            f"\n{jogador.nome} | "
            f"❤️ {jogador.vida}/{jogador.vida_max} | "
            f"🔮 {jogador.mana}/{jogador.mana_max} | "
            f"⭐ Nv {jogador.nivel} | "
            f"🪙 Ouro: {jogador.ouro}"
        )

        print(f"{inimigo.nome} | HP: {inimigo.vida}")

        jogador.defendendo = False

        print("\nEscolha sua ação:")
        print("1 - Atacar")
        print("2 - Habilidade")
        print("3 - Defender")
        print("4 - Inventário")

        entrada = input(">>> ")

        if not entrada.isdigit():
            print("❌ Digite um número válido.")
            continue

        escolha = int(entrada)

        if escolha < 1 or escolha > 4:
            print("❌ Opção inválida.")
            continue

        # AÇÕES DO JOGADOR
        if escolha == 1:
            jogador.ataque_normal(inimigo)

        elif escolha == 2:
            jogador.habilidade(inimigo)

        elif escolha == 3:
            jogador.defendendo = True
            print("🛡️ Você está se defendendo!")

        elif escolha == 4:
            usar_item(jogador)
            continue  # usar item não consome turno do inimigo

        # TURNO DO INIMIGO
        if inimigo.esta_vivo():
            inimigo.atacar(jogador)

    return jogador.esta_vivo()
