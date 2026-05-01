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

        # Lógica de Diálogos
        if quest.entregue:
            msg = quest.dialogos.get("entregue", "Obrigado pela ajuda!")
            print(f"{self.nome}: {msg}")

        elif quest.concluida:
            msg = quest.dialogos.get("concluida", "Incrível! Você conseguiu.")
            print(f"{self.nome}: {msg}")
            quest.entregar(jogador) 

        elif quest.aceita:
            msg = quest.dialogos.get("progresso", "Como vai a missão?")
            print(f"{self.nome}: {msg} ({quest.progresso}/{quest.quantidade})")

        else:
            msg = quest.dialogos.get("inicio", quest.descricao)
            print(f"{self.nome}: {msg}")
            
            confirmar = input("Aceitar missão? (s/n): ").lower()
            if confirmar == 's':
                quest.aceita = True
                print("📜 Missão aceita!")
            else:
                print(f"{self.nome}: Entendo. Volte se mudar de ideia.")