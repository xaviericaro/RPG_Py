import random
from core.inimigo import Inimigo
from systems.batalha import batalha
from persistence.save import salvar_jogo
from systems.loja import loja
from systems.npc import NPC, Quest

MAPA = {
    "Vilarejo": {
        "descricao": "Um vilarejo tranquilo, com pessoas amigáveis.",
        "opcoes": ["Falar com o Ancião", "Ir à Loja", "Descansar", "Ir para a Floresta"],
        "destinos": ["Vilarejo", "Vilarejo", "Vilarejo", "Floresta"]
    },
    "Floresta": {
        "descricao": "Uma floresta sombria cheia de perigos.",
        "opcoes": ["Explorar", "Voltar ao Vilarejo", "Seguir para a Montanha"],
        "destinos": ["Floresta", "Vilarejo", "Montanha"]
    },
    "Montanha": {
        "descricao": "Uma montanha onde o Dragão Ancião habita.",
        "opcoes": ["Enfrentar o Dragão", "Voltar para a Floresta"],
        "destinos": ["Montanha", "Floresta"]
    }
    
}


def inimigo_aleatorio(area):
    if area == "Floresta":
        return random.choice([
            Inimigo("Goblin", 50, 10, 4, 30),
            Inimigo("Lobo Sombrio", 80, 18, 7, 60),
        ])

    if area == "Montanha":
        return Inimigo("Dragão Ancião", 250, 35, 15, 300)

    return None

npc_vilarejo = NPC(
    "Ancião do Vilarejo",
    Quest(
        "Derrote um inimigo na floresta e volte até mim.",
        objetivo="derrotar_floresta",
        recompensa_ouro=50,
    ),
)


def loop_mapa(jogador, area_atual):
    while True:
        area = MAPA[area_atual]

        print(f"\n📍 {area_atual}")
        print(area["descricao"])
        print(f"❤️ HP: {jogador.vida}/{jogador.vida_max} | "
            f"🔮 MP: {jogador.mana}/{jogador.mana_max} | "
            f"⭐ Nível: {jogador.nivel} | "
            f"XP: {jogador.xp}/{jogador.xp_para_proximo}")

        for i, opcao in enumerate(area["opcoes"]):
            print(f"{i+1} - {opcao}")

        escolha = int(input(">>> ")) - 1

        if escolha < 0 or escolha >= len(area["opcoes"]):
            print("Escolha inválida!")
            continue

        # DESCANSAR
        if area["opcoes"][escolha] == "Descansar":
            jogador.vida = jogador.vida_max
            jogador.mana = jogador.mana_max
            print("😴 Você descansou e recuperou tudo!")
            salvar_jogo(jogador, area_atual)
            continue

        if area_atual == "Vilarejo":
            if area["opcoes"][escolha] == "Falar com o Ancião":
                npc_vilarejo.falar(jogador)
                continue

        if area["opcoes"][escolha] == "Ir à Loja":
            loja(jogador)
            continue


        # EXPLORAR
        if "Explorar" in area["opcoes"][escolha]:
            inimigo = inimigo_aleatorio(area_atual)
            if inimigo:
                venceu = batalha(jogador, inimigo)
                if not venceu:
                    print("💀 Você morreu na exploração...")
                    salvar_jogo(jogador, area_atual)
                    return
                jogador.ganhar_xp(inimigo.xp_drop)
                jogador.ouro += inimigo.ouro_drop
                print(f"💰 Ganhou {inimigo.ouro_drop} ouro!")

                print(f"⭐ Ganhou {inimigo.xp_drop} XP!")
                salvar_jogo(jogador, area_atual)
            else:
                print("Nada aconteceu...")
            continue

        # DRAGÃO FINAL
        if area_atual == "Montanha" and area["opcoes"][escolha] == "Enfrentar o Dragão":
            dragao = inimigo_aleatorio("Montanha")
            venceu = batalha(jogador, dragao)
            if venceu:
                print("🏆 VOCÊ DERROTOU O DRAGÃO E SALVOU O MUNDO!")
            else:
                print("💀 O Dragão foi forte demais...")
            salvar_jogo(jogador, area_atual)
            return

        # MUDAR DE ÁREA
        area_atual = area["destinos"][escolha]
        salvar_jogo(jogador, area_atual)

