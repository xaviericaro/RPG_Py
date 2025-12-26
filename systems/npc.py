from systems.quest_system import Quest
class Quest:
    def __init__(self, quest_id, descricao, area_objetivo, quantidade, recompensa_ouro):
        self.id = quest_id
        self.descricao = descricao
        self.area_objetivo = area_objetivo
        self.quantidade = quantidade
        self.progresso = 0
        self.recompensa_ouro = recompensa_ouro
        self.aceita = False
        self.concluida = False
        self.entregue = False

    def registrar_evento(self, area):
        if not self.aceita or self.concluida or self.entregue:
            return


        if area == self.area_objetivo:
            self.progresso += 1
            print(f"📜 Progresso da quest: {self.progresso}/{self.quantidade}")

            if self.progresso >= self.quantidade:
                self.concluida = True
                print("✅ Quest concluída! Volte ao NPC.")


class NPC:
    def __init__(self, nome, quest_id):
        self.nome = nome
        self.quest_id = quest_id

    def falar(self, jogador):
        # 🔐 proteção importante
        if self.quest_id not in jogador.quests:
            print("❓ Não tenho nenhuma missão para você agora.")
            return

        quest = jogador.quests[self.quest_id]

        print(f"\n🧑 {self.nome}:")

        if quest.entregue:
            print("Obrigado novamente, herói.")
            return

        if not quest.aceita:
            print(quest.descricao)
            if input("Aceitar quest? (s/n) ").lower() == "s":
                quest.aceita = True
                print("📜 Quest aceita!")
            return

        if quest.concluida:
            print("🎉 Excelente trabalho!")
            jogador.ouro += quest.recompensa["ouro"]
            jogador.ganhar_xp(quest.recompensa["xp"])
            quest.entregue = True
            return

        print("Continue sua missão.")

