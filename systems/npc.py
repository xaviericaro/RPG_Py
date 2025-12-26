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

        # 1. Quest Finalizada (Entregue)
        if quest.entregue:
            fala = quest.dialogos.get("entregue", "Obrigado pela ajuda de antes!")
            print(f"{self.nome}: {fala}")
            return

        # 2. Quest Concluída mas não entregue (Momento da recompensa)
        if quest.concluida:
            fala = quest.dialogos.get("concluida", "Excelente trabalho! Aqui está sua recompensa.")
            print(f"{self.nome}: {fala}")
            
            if not quest.entregue:
                jogador.ouro += quest.recompensa_ouro
                quest.entregue = True
                print(f"💰 Recompensa: +{quest.recompensa_ouro} ouro!")
            return

        # 3. Quest já aceita, mas em andamento (Progresso)
        if quest.aceita:
            fala = quest.dialogos.get("progresso", f"Como vai a missão? ({quest.progresso}/{quest.quantidade})")
            print(f"{self.nome}: {fala}")
            return

        # 4. Quest disponível (Início)
        fala_inicio = quest.dialogos.get("inicio", quest.descricao)
        print(f"{self.nome}: {fala_inicio}")
        
        aceitar = input("Aceitar a quest? (s/n): ").lower()
        if aceitar == "s":
            quest.aceita = True
            print(f"📜 Quest '{quest.id}' aceita!")
        else:
            print(f"{self.nome}: Talvez outra hora.")