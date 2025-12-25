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

    def registrar_evento(self, area):
        if not self.aceita or self.concluida:
            return

        if area == self.area_objetivo:
            self.progresso += 1
            print(f"📜 Progresso da quest: {self.progresso}/{self.quantidade}")

            if self.progresso >= self.quantidade:
                self.concluida = True
                print("✅ Quest concluída! Volte ao NPC.")


class NPC:
    def __init__(self, nome, quest: Quest):
        self.nome = nome
        self.quest = quest

    def falar(self, jogador):
        print(f"\n🧑 {self.nome}:")

        if not self.quest.aceita:
            print(self.quest.descricao)
            print("1 - Aceitar quest")
            print("0 - Sair")
            escolha = input(">>> ")

            if escolha == "1":
                self.quest.aceita = True
                print("📜 Quest aceita!")
            return

        if self.quest.concluida:
            print("🎉 Você conseguiu! Aqui está sua recompensa.")
            jogador.ouro += self.quest.recompensa_ouro
            print(f"💰 Ganhou {self.quest.recompensa_ouro} ouro!")
            self.quest.concluida = False  # impede repetir
            return

        print("Ainda não terminou sua missão...")
