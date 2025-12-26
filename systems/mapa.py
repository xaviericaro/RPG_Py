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

def ferreiro(jogador):
    """Sistema de Crafting: troca materiais por equipamentos."""
    while True:
        print(f"\n" + "⚒️ " * 5 + " FORJA DO VILAREJO " + "⚒️ " * 5)
        print(f"🪙 Ouro: {jogador.ouro}")
        
        # Contagem de materiais para o jogador ver
        materiais = {}
        for item in jogador.inventario:
            if item.get("tipo") == "material":
                nome = item["nome"]
                materiais[nome] = materiais.get(nome, 0) + 1
        
        print(f"📦 Seus Materiais: {materiais if materiais else 'Vazio'}")
        print("-" * 40)
        print("1 - Espada de Ferro (Custo: 3x Minério de Ferro + 50 Ouro)")
        print("2 - Armadura de Couro (Custo: 4x Pele de Lobo + 40 Ouro)")
        print("0 - Sair")
        
        escolha = input("\nO que deseja fabricar? >>> ")

        if escolha == "1":
            qtd_minerio = materiais.get("Minério de Ferro", 0)
            if qtd_minerio >= 3 and jogador.ouro >= 50:
                # Pagamento
                jogador.ouro -= 50
                removidos = 0
                idx = 0
                while removidos < 3:
                    if jogador.inventario[idx]["nome"] == "Minério de Ferro":
                        jogador.inventario.pop(idx)
                        removidos += 1
                    else:
                        idx += 1
                
                # Item novo
                espada_ferro = {"nome": "Espada de Ferro", "tipo": "arma", "ataque": 15, "valor": 100}
                jogador.inventario.append(espada_ferro)
                print("\n🔥 O Ferreiro martela o ferro quente... TING! TING! TING!")
                print("⚔️ Você recebeu uma [Espada de Ferro]!")
            else:
                print("\n❌ Materiais ou Ouro insuficientes!")
        elif escolha == "0":
            break

            # --- LÓGICA DA ARMADURA DE COURO ---
        elif escolha == "2":
            qtd_pele = materiais.get("Pele de Lobo", 0)
            if qtd_pele >= 4 and jogador.ouro >= 40:
                # Pagamento
                jogador.ouro -= 40
                removidos = 0
                idx = 0
                while removidos < 4:
                    if jogador.inventario[idx]["nome"] == "Pele de Lobo":
                        jogador.inventario.pop(idx)
                        removidos += 1
                    else:
                        idx += 1
                
                # Criando a Armadura
                armadura_couro = {
                    "nome": "Armadura de Couro", 
                    "tipo": "armadura", 
                    "defesa": 10, 
                    "valor": 80
                }
                jogador.inventario.append(armadura_couro)
                print("\n🧵 O Ferreiro costura as peles com maestria...")
                print("🛡️ Você recebeu uma [Armadura de Couro]!")
            else:
                print("\n❌ Materiais ou Ouro insuficientes!")

        elif escolha == "0":
            break
def inimigo_aleatorio(area):
    if area == "Floresta":
        return random.choice([
            Inimigo("Goblin", 50, 10, 4, 30, 10, 
                    [{"nome": "Tecido Rasgado", "tipo": "material", "valor": 5}]),
            Inimigo("Orc Brutal", 70, 15, 6, 80, 15, 
                    [{"nome": "Minério de Ferro", "tipo": "material", "valor": 15}]),
            Inimigo("Lobo Sombrio", 80, 18, 7, 60, 20, 
                    [{"nome": "Pele de Lobo", "tipo": "material", "valor": 10}]),
        ])
    if area == "Montanha":
        return Inimigo("Dragão Ancião", 250, 35, 15, 300, 200, 
                       [{"nome": "Escama de Dragão", "tipo": "material", "valor": 100}])
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
            "Ferreiro (Crafting)",
            "Ir para a Floresta",
        ],
        "destinos": [
            None, None, None, None, None, "Floresta"
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

        # Equipamentos atuais para exibição
        arma_nome = jogador.arma["nome"] if jogador.arma else "Mãos Nuas"
        armor_nome = jogador.armadura["nome"] if jogador.armadura else "Trapos"

        print(f"\n📍 {area_atual.upper()}")
        print(f"📜 {area['descricao']}")
        print(
            f"❤️  HP: {jogador.vida}/{jogador.vida_max} | 🔮 MP: {jogador.mana}/{jogador.mana_max}\n"
            f"⭐ NV: {jogador.nivel} | 🪙 Ouro: {jogador.ouro}\n"
            f"⚔️ Arma: {arma_nome} | 🛡️ Armadura: {armor_nome}" # STATUS DE EQUIPE
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

        elif opcao_texto == "Ferreiro (Crafting)":
            ferreiro(jogador)
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
            
            # --- SISTEMA DE LOOT DINÂMICO ---
            if inimigo.possiveis_drops:
                if random.random() < 0.5:
                    item_ganho = random.choice(inimigo.possiveis_drops).copy()
                    jogador.inventario.append(item_ganho)
                    print(f"📦 LOOT: Você encontrou [{item_ganho['nome']}]!")

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