import random
from core.inimigo import Inimigo
from systems.batalha import batalha
from persistence.save import salvar_jogo
from systems.loja import loja
from systems.npc import NPC

# =========================
# FUNÇÕES DE APOIO
# =========================

def menu_atributos(jogador):
    """Interface para o jogador distribuir pontos ganhos ao subir de nível."""
    while jogador.pontos_disponiveis > 0:
        print(f"\n" + "="*35)
        print(f"✨ PONTOS DISPONÍVEIS: {jogador.pontos_disponiveis}")
        print(f"1 - Força (+2 Ataque) [Atual: {jogador.ataque}]")
        print(f"2 - Agilidade (+2 Defesa) [Atual: {jogador.defesa}]")
        print(f"3 - Vitalidade (+10 HP Máx) [Atual: {jogador.vida_max}]")
        print(f"4 - Inteligência (+10 Mana Máx) [Atual: {jogador.mana_max}]")
        print(f"0 - Sair")
        print("="*35)
        
        escolha = input("Escolha onde investir: ")

        if escolha == "1":
            jogador.ataque += 2
            jogador.pontos_disponiveis -= 1
        elif escolha == "2":
            jogador.defesa += 2
            jogador.pontos_disponiveis -= 1
        elif escolha == "3":
            jogador.vida_max += 10
            jogador.vida += 10 
            jogador.pontos_disponiveis -= 1
        elif escolha == "4":
            jogador.mana_max += 10
            jogador.mana += 10
            jogador.pontos_disponiveis -= 1
        elif escolha == "0":
            break
        else:
            print("❌ Opção inválida!")
    
    if jogador.pontos_disponiveis == 0:
        print("\n✅ Todos os pontos foram distribuídos!")

def inimigo_aleatorio(area):
    if area == "Floresta":
        return random.choice([
            Inimigo("Goblin", 50, 10, 4, 30, 10),
            Inimigo("Orc Brutal", 70, 15, 6, 80, 15),
            Inimigo("Lobo Sombrio", 80, 18, 7, 60, 20),
        ])
    if area == "Montanha":
        return Inimigo("Dragão Ancião", 250, 35, 15, 300, 200)
    return None

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
            "Distribuir Pontos",
            "Ir para a Floresta",
        ],
        "destinos": [
            None, None, None, None, "Floresta"
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
            None, "Vilarejo", "Montanha"
        ],
    },
    "Montanha": {
        "descricao": "Uma montanha onde o Dragão Ancião habita.",
        "opcoes": [
            "Enfrentar o Dragão",
            "Voltar para a Floresta",
        ],
        "destinos": [
            None, "Floresta"
        ],
    },
}

npc_vilarejo = NPC(nome="Ancião do Vilarejo", quest_id="limpar_floresta")

# =========================
# LOOP DO MAPA
# =========================
def loop_mapa(jogador, area_atual):
    while True:
        area = MAPA[area_atual]

        print(f"\n📍 {area_atual.upper()}")
        print(f"📜 {area['descricao']}")
        print(
            f"❤️  HP: {jogador.vida}/{jogador.vida_max} | "
            f"🔮 MP: {jogador.mana}/{jogador.mana_max} | "
            f"⭐ NV: {jogador.nivel} | "
            f"🪙 Ouro: {jogador.ouro}"
        )

        for i, opcao in enumerate(area["opcoes"], start=1):
            print(f"{i} - {opcao}")

        entrada = input("\nO que deseja fazer? >>> ")
        if not entrada.isdigit():
            print("❌ Digite um número válido.")
            continue

        escolha_idx = int(entrada) - 1

        if escolha_idx < 0 or escolha_idx >= len(area["opcoes"]):
            print("❌ Opção inválida.")
            continue

        opcao_texto = area["opcoes"][escolha_idx]
        destino = area["destinos"][escolha_idx]

        # --- AÇÕES ESPECIAIS (NÃO MUDAM DE ÁREA) ---
        if opcao_texto == "Falar com o Ancião":
            npc_vilarejo.falar(jogador)
            salvar_jogo(jogador, area_atual)
            continue

        elif opcao_texto == "Ir à Loja":
            loja(jogador)
            salvar_jogo(jogador, area_atual)
            continue

        elif opcao_texto == "Descansar":
            jogador.vida = jogador.vida_max
            jogador.mana = jogador.mana_max
            print("\n😴 Você descansou e recuperou suas energias!")
            salvar_jogo(jogador, area_atual)
            continue

        elif opcao_texto == "Distribuir Pontos":
            menu_atributos(jogador)
            salvar_jogo(jogador, area_atual)
            continue

        elif opcao_texto == "Explorar":
            inimigo = inimigo_aleatorio(area_atual)
            
            # Introdução da História
            from systems.historia import encontro_goblin, encontro_orc, encontro_lobo
            if inimigo.nome == "Goblin": encontro_goblin()
            elif inimigo.nome == "Orc Brutal": encontro_orc()
            elif inimigo.nome == "Lobo Sombrio": encontro_lobo()

            venceu = batalha(jogador, inimigo)
            if not venceu:
                print("💀 Game Over...")
                return

            jogador.ganhar_xp(inimigo.xp_drop)
            jogador.ouro += inimigo.ouro_drop
            
            # Registrar progresso de quests
            for quest in jogador.quests.values():
                quest.registrar_evento(area_atual)

            salvar_jogo(jogador, area_atual)
            continue

        elif opcao_texto == "Enfrentar o Dragão":
            from systems.historia import chegada_montanha, final_vitoria
            chegada_montanha()
            dragao = inimigo_aleatorio("Montanha")
            if batalha(jogador, dragao):
                final_vitoria()
                return
            else:
                print("💀 O Dragão derrotou você.")
                return

        # --- MUDANÇA DE ÁREA (DESTINOS) ---
        if destino:
            if destino == "Montanha":
                quest_f = jogador.quests.get("limpar_floresta")
                if not quest_f or not quest_f.entregue:
                    print("\n🚫 O caminho para a Montanha está selado!")
                    print("Dica: Complete a quest do Ancião primeiro.")
                    input("Pressione Enter...")
                    continue

            area_atual = destino
            print(f"\n✈️  Viajando para {area_atual}...")
            salvar_jogo(jogador, area_atual)