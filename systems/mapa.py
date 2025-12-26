import random
from core.inimigo import Inimigo
from systems.batalha import batalha
from persistence.save import salvar_jogo
from systems.loja import loja
from systems.npc import NPC


# =========================
# MAPA DO JOGO
# =========================
MAPA = {
    "Vilarejo": {
        "descricao": "Um vilarejo tranquilo, com pessoas amigáveis.",
        "opcoes": [
            "Falar com o Ancião",
            "Ir à Loja",
            "Descansar",
            "Ir para a Floresta",
        ],
        "destinos": [
            None,
            None,
            None,
            "Floresta",
        ],
    },
    "Floresta": {
        "descricao": "Uma floresta sombria cheia de perigos.",
        "opcoes": [
            "Explorar",
            "Voltar ao Vilarejo",
            "Seguir para a Montanha",
        ],
        "destinos": [
            None,
            "Vilarejo",
            "Montanha",
        ],
    },
    "Montanha": {
        "descricao": "Uma montanha onde o Dragão Ancião habita.",
        "opcoes": [
            "Enfrentar o Dragão",
            "Voltar para a Floresta",
        ],
        "destinos": [
            None,
            "Floresta",
        ],
    },
}


# =========================
# NPCs
# =========================
npc_vilarejo = NPC(
    nome="Ancião do Vilarejo",
    quest_id="limpar_floresta",
)


# =========================
# INIMIGOS
# =========================
def inimigo_aleatorio(area):
    if area == "Floresta":
        return random.choice(
            [
                Inimigo("Goblin", 50, 10, 4, 30, 10),
                Inimigo("Orc Brutal", 70, 15, 6, 80, 15),
                Inimigo("Lobo Sombrio", 80, 18, 7, 60, 20),
            ]
        )

    if area == "Montanha":
        return Inimigo("Dragão Ancião", 250, 35, 15, 300, 200)

    return None


# =========================
# LOOP DO MAPA
# =========================
def loop_mapa(jogador, area_atual):
    while True:
        area = MAPA[area_atual]

        print(f"\n📍 {area_atual}")
        print(area["descricao"])
        print(
            f"❤️ {jogador.vida}/{jogador.vida_max} | "
            f"🔮 {jogador.mana}/{jogador.mana_max} | "
            f"⭐ Nv {jogador.nivel} | "
            f"XP {jogador.xp}/{jogador.xp_para_proximo} | "
            f"🪙 Ouro {jogador.ouro}"
        )

        for i, opcao in enumerate(area["opcoes"], start=1):
            print(f"{i} - {opcao}")

        entrada = input(">>> ")

        if not entrada.isdigit():
            print("❌ Digite um número válido.")
            continue

        escolha = int(entrada) - 1

        if escolha < 0 or escolha >= len(area["opcoes"]):
            print("❌ Opção inválida.")
            continue

        opcao_escolhida = area["opcoes"][escolha]

        # =========================
        # VILAREJO
        # =========================
        if area_atual == "Vilarejo":
            if opcao_escolhida == "Falar com o Ancião":
                npc_vilarejo.falar(jogador)
                salvar_jogo(jogador, area_atual)
                continue

            if opcao_escolhida == "Ir à Loja":
                loja(jogador)
                salvar_jogo(jogador, area_atual)
                continue

            if opcao_escolhida == "Descansar":
                jogador.vida = jogador.vida_max
                jogador.mana = jogador.mana_max
                print("😴 Você descansou e recuperou tudo!")
                salvar_jogo(jogador, area_atual)
                continue

        # =========================
        # EXPLORAR / BATALHA
        # =========================
        if opcao_escolhida == "Explorar":
            inimigo = inimigo_aleatorio(area_atual)

            if not inimigo:
                print("Nada aconteceu...")
                continue

            # história antes da batalha
            from systems.historia import encontro_goblin, encontro_orc, encontro_lobo

            if inimigo.nome == "Goblin":
                encontro_goblin()
            elif inimigo.nome == "Orc Brutal":
                encontro_orc()
            elif inimigo.nome == "Lobo Sombrio":
                encontro_lobo()
            else:
                print(f"\n⚔️ Um {inimigo.nome} bloqueia seu caminho!")

            venceu = batalha(jogador, inimigo)

            if not venceu:
                print("💀 Você morreu...")
                salvar_jogo(jogador, area_atual)
                return

            jogador.ganhar_xp(inimigo.xp_drop)
            jogador.ouro += inimigo.ouro_drop

            print(f"⭐ Ganhou {inimigo.xp_drop} XP!")
            print(f"🪙 Ganhou {inimigo.ouro_drop} ouro!")

            for quest in jogador.quests.values():
                quest.registrar_evento(area_atual)

            salvar_jogo(jogador, area_atual)
            continue

        # =========================
        # DRAGÃO FINAL
        # =========================
        if area_atual == "Montanha" and opcao_escolhida == "Enfrentar o Dragão":
            from systems.historia import chegada_montanha, final_vitoria

            chegada_montanha()

            dragao = inimigo_aleatorio("Montanha")
            venceu = batalha(jogador, dragao)

            if venceu:
                final_vitoria()
            else:
                print("💀 O Dragão foi forte demais para você...")

            salvar_jogo(jogador, area_atual)
            return

        # =========================
        # MUDAR DE ÁREA
        # =========================
        destino = area["destinos"][escolha]
        if destino:
            if destino == "Montanha":
                quest_floresta = jogador.quests.get("limpar_floresta")
                
                # Se a quest não existe ou não foi entregue, bloqueia
                if not quest_floresta or not quest_floresta.entregue:
                    print("\n" + "!"*30)
                    print("🚫 CAMINHO BLOQUEADO!")
                    print("O guarda da fronteira diz: 'Somente heróis autorizados pelo Ancião passam para a Montanha!'")
                    print("!"*30)
                    input("\nPressione Enter para voltar...")
                    continue

            area_atual = destino
            print(f"\n✈️ Viajando para {area_atual}...")
            salvar_jogo(jogador, area_atual)
