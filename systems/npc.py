class NPC:
    def __init__(self, nome, quest_id=None):
        self.nome = nome
        self.quest_id = quest_id

    def falar(self, jogador):
        if not self.quest_id:
            print(f"{self.nome}: Olá, viajante.")
            return

        quest = jogador.quests.get(self.quest_id)

        if not quest:
            print(f"{self.nome}: Não tenho nada para você agora.")
            return

        # --- LÓGICA DE DIÁLOGOS DINÂMICOS ---

        # 1. Já terminou tudo
        if quest.entregue:
            msg = quest.dialogos.get("entregue", "Obrigado pela ajuda!")
            print(f"{self.nome}: {msg}")

        # 2. Completou os objetivos, mas não recebeu a recompensa
        elif quest.concluida:
            msg = quest.dialogos.get("concluida", "Incrível! Você conseguiu.")
            print(f"{self.nome}: {msg}")
            # Chama o método de entrega que você já tem no quest_system
            quest.entregar(jogador) 

        # 3. Está no meio da missão
        elif quest.aceita:
            msg = quest.dialogos.get("progresso", "Como vai a missão?")
            print(f"{self.nome}: {msg} ({quest.progresso}/{quest.quantidade})")

        # 4. Primeira vez falando (Oferecer a quest)
        else:
            msg = quest.dialogos.get("inicio", quest.descricao)
            print(f"{self.nome}: {msg}")
            
            confirmar = input("Aceitar missão? (s/n): ").lower()
            if confirmar == 's':
                quest.aceita = True
                print("📜 Missão aceita!")
            else:
                print(f"{self.nome}: Entendo. Volte se mudar de ideia.")