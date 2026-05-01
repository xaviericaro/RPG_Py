import random
from core.inimigo import Inimigo
from systems.batalha import batalha
from persistence.save import salvar_jogo
from systems.loja import loja
from systems.npc import NPC
from data.database import ITENS, RECEITAS, LISTA_INIMIGOS

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


def executar_crafting(jogador):
    """Lógica interna para fabricar itens."""
    from data.database import ITENS, RECEITAS
    
    materiais_jogador = {}
    for it in jogador.inventario:
        materiais_jogador[it["nome"]] = materiais_jogador.get(it["nome"], 0) + 1

    opcoes_craft = list(RECEITAS.keys())
    print("\n--- OFICINA DE CRIAÇÃO ---")
    for i, nome_item in enumerate(opcoes_craft, start=1):
        rec = RECEITAS[nome_item]
        req_txt = " + ".join([f"{q}x {m}" for m, q in rec['materiais'].items()])
        print(f"{i} - {nome_item}")
        print(f"    👉 Requer: {req_txt} | Custo: {rec['custo_ouro']}g")

    print("0 - Voltar")
    escolha = input("\nO que deseja fabricar? >>> ")

    if escolha == "0" or not escolha.isdigit():
        return

    idx = int(escolha) - 1
    if idx < 0 or idx >= len(opcoes_craft):
        print("❌ Opção inválida.")
        return

    nome_alvo = opcoes_craft[idx]
    receita = RECEITAS[nome_alvo]

    pode_fazer = True
    if jogador.ouro < receita["custo_ouro"]:
        pode_fazer = False
    
    for mat, qtd_necessaria in receita["materiais"].items():
        if materiais_jogador.get(mat, 0) < qtd_necessaria:
            pode_fazer = False
            break

    if pode_fazer:
        jogador.ouro -= receita["custo_ouro"]
        
        for mat, qtd_necessaria in receita["materiais"].items():
            removidos = 0
            while removidos < qtd_necessaria:
                for j, item_inv in enumerate(jogador.inventario):
                    if item_inv["nome"] == mat:
                        jogador.inventario.pop(j)
                        removidos += 1
                        break
        
        novo_item = ITENS[nome_alvo].copy()
        novo_item["nome"] = nome_alvo
        jogador.inventario.append(novo_item)
        print(f"\n✅ Sucesso! Você fabricou: [{nome_alvo}]!")
    else:
        print("\n❌ Você não possui materiais ou ouro suficientes!")

def ferreiro(jogador):
    """Menu principal do Ferreiro."""
    while True:
        print(f"\n" + "⚒️ " * 3 + " FORJA DO VILAREJO " + "⚒️ " * 3)
        print(f"🪙 Seu Ouro: {jogador.ouro}")
        print("-" * 30)
        print("1 - Fabricar Itens (Crafting)")
        print("2 - Reparar Equipamentos")
        print("0 - Sair")
        
        escolha = input("\nO que deseja fazer? >>> ")

        if escolha == "1":
            executar_crafting(jogador)

        elif escolha == "2":
            itens_para_reparar = []
            if jogador.arma: itens_para_reparar.append(("arma", jogador.arma))
            if jogador.armadura: itens_para_reparar.append(("armadura", jogador.armadura))

            if not itens_para_reparar:
                print("\n❌ Você não tem nada equipado para consertar!")
                continue

            print("\n🔧 SELECIONE O ITEM PARA REPARAR:")
            for i, (tipo, item) in enumerate(itens_para_reparar, start=1):
                falta = 100 - item.get("durabilidade", 100)
                custo = falta // 2 
                print(f"{i} - {item['nome']} ({item.get('durabilidade', 100)}% DUR | Custo: {custo}g)")

            op = input("\nEscolha o item ou 0 para voltar: ")
            if op.isdigit() and 0 < int(op) <= len(itens_para_reparar):
                tipo, item_sel = itens_para_reparar[int(op)-1]
                falta = 100 - item_sel.get("durabilidade", 100)
                custo = falta // 2

                if custo == 0:
                    print(f"\n✨ {item_sel['nome']} está como nova!")
                elif jogador.ouro >= custo:
                    jogador.ouro -= custo
                    item_sel["durabilidade"] = 100
                    print(f"\n🔥 O Ferreiro martelou e poliu seu item! {item_sel['nome']} restaurada.")
                else:
                    print("\n❌ Ouro insuficiente para o reparo!")

        elif escolha == "0":
            break

def inimigo_aleatorio(area):
    dados_inimigo = random.choice(LISTA_INIMIGOS[area])
    
    possiveis_drops = []
    for nome_item in dados_inimigo["drops"]:
        item_info = ITENS[nome_item].copy()
        item_info["nome"] = nome_item
        possiveis_drops.append(item_info)

    return Inimigo(
        dados_inimigo["nome"],
        dados_inimigo["hp"],
        dados_inimigo["atk"],
        dados_inimigo["def"],
        dados_inimigo["xp"],
        dados_inimigo["ouro"],
        possiveis_drops
    )

MAPA = {
    "Vilarejo": {
        "descricao": "Um vilarejo tranquilo, com pessoas amigáveis.",
        "opcoes": [
            "Falar com o Ancião",
            "Ir à Loja",
            "Descansar",
            "Distribuir Pontos",
            "Ferreiro (Crafting)",
            "Salvar e Sair",
            "Ir para a Floresta",
        ],
        "destinos": [
            None, None, None, None, None, None, "Floresta"
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

def loop_mapa(jogador, area_atual):
    while True:
        area = MAPA[area_atual]

        arma_nome = jogador.arma["nome"] if jogador.arma else "Mãos Nuas"
        armor_nome = jogador.armadura["nome"] if jogador.armadura else "Trapos"

        print(f"\n📍 {area_atual.upper()}")
        print(f"📜 {area['descricao']}")
        print(
            f"❤️  HP: {jogador.vida}/{jogador.vida_max} | 🔮 MP: {jogador.mana}/{jogador.mana_max}\n"
            f"⭐ NV: {jogador.nivel} | 🪙 Ouro: {jogador.ouro}\n"
            f"⚔️ Arma: {arma_nome} | 🛡️ Armadura: {armor_nome}"
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

        elif opcao_texto == "Salvar e Sair":
            salvar_jogo(jogador, area_atual)
            print("\n💾 Jogo salvo com sucesso! Até a próxima aventura!")
            return

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
            
            # Loot dinâmico
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