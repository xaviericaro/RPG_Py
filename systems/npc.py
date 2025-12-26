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

        # Quest ainda não aceita
        if not quest.aceita:
            print(f"{self.nome}: {quest.descricao}")
            aceitar = input("Aceitar a quest? (s/n): ").lower()

            if aceitar == "s":
                quest.aceita = True
                print("📜 Quest aceita!")
            else:
                print(f"{self.nome}: Talvez outra hora.")
            return

        # Quest concluída mas não entregue
        if quest.concluida and not quest.entregue:
            print(f"{self.nome}: Excelente trabalho!")
            jogador.ouro += quest.recompensa_ouro
            quest.entregue = True
            print(f"💰 Você recebeu {quest.recompensa_ouro} ouro!")
            return

        # Quest em andamento
        print(f"{self.nome}: Continue sua missão.")
