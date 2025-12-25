class Quest:
    def __init__(self, descricao, objetivo, recompensa_ouro):
        self.descricao = descricao
        self.objetivo = objetivo
        self.recompensa_ouro = recompensa_ouro
        self.concluida = False


class NPC:
    def __init__(self, nome, quest: Quest):
        self.nome = nome
        self.quest = quest

    def falar(self, jogador):
        print(f"\n🧑 {self.nome}:")

        if not self.quest.concluida:
            print(self.quest.descricao)
            print("1 - Aceitar quest")
            print("0 - Sair")

            escolha = input(">>> ")
            if escolha == "1":
                print("📜 Quest aceita!")
        else:
            print("Obrigado novamente, herói!")
