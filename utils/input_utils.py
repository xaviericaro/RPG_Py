def escolher_opcao(max_opcoes):
    entrada = input(">>> ")
    if not entrada.isdigit():
        return None

    escolha = int(entrada) - 1
    if escolha < 0 or escolha >= max_opcoes:
        return None

    return escolha
