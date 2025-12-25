from core.inimigo import Inimigo
from systems.batalha import batalha
from persistence.save import salvar_jogo

def modo_historia(jogador, progresso):
    inimigos = [
        Inimigo("Goblin", 50, 10, 4, 30),
        Inimigo("Orc Brutal", 90, 15, 6, 50),
        Inimigo("Lobo Sombrio", 80, 18, 7, 60),
        Inimigo("Dragão Ancião - Fase 1", 150, 25, 10, 100),
        Inimigo("Dragão Ancião - Fase 2", 220, 30, 14, 200),
    ]

    for i in range(progresso, len(inimigos)):
        venceu = batalha(jogador, inimigos[i])

        if not venceu:
            salvar_jogo(jogador, i)
            print("💀 Você foi derrotado...")
            return

        jogador.xp += inimigos[i].xp_drop
        print(f"⭐ Ganhou {inimigos[i].xp_drop} XP!")
        salvar_jogo(jogador, i + 1)

    print("🏆 Você concluiu a história!")
