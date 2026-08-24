class NPC:
    def __init__(self, nome, quest_ids=None, saudacao="Olá, viajante."):
        self.nome = nome
        # Lista ordenada de missões (permite cadeias: a próxima só aparece
        # quando a anterior já foi entregue).
        if quest_ids is None:
            quest_ids = []
        elif isinstance(quest_ids, str):
            quest_ids = [quest_ids]
        self.quest_ids = quest_ids
        self.saudacao = saudacao

    def _quest_ativa(self, jogador):
        for qid in self.quest_ids:
            quest = jogador.quests.get(qid)
            if quest and not quest.entregue:
                return quest
        return None

    def falar(self, jogador):
        quest = self._quest_ativa(jogador)

        if not quest:
            print(f"{self.nome}: {self.saudacao}")
            return

        # Para quests de item, verifica se o jogador já cumpre o requisito
        quest.verificar_item(jogador)

        if quest.concluida and not quest.entregue:
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
            if confirmar == "s":
                quest.aceita = True
                print("📜 Missão aceita!")
                quest.verificar_item(jogador)
                if quest.concluida:
                    print(f"{self.nome}: Ora, você já tem o que preciso!")
                    quest.entregar(jogador)
            else:
                print(f"{self.nome}: Entendo. Volte se mudar de ideia.")
