import pygame
import sys
import os

from core.jogador import Guerreiro, Mago
from persistence.save import definir_save, salvar_jogo, carregar_jogo
from systems.mapa import inimigo_aleatorio
from data.database import ITENS, RECEITAS, MAPA, LISTA_INIMIGOS

# === CONFIGURAÇÕES ===
LARGURA, ALTURA = 800, 600
FPS = 60

# Cores
PRETO = (20, 20, 20)
BRANCO = (255, 255, 255)
VERDE = (50, 200, 50)
VERMELHO = (200, 50, 50)
AZUL = (50, 50, 200)
OURO = (255, 215, 0)
CINZA = (70, 70, 70)
ROXO = (150, 0, 200)

# === CLASSE BOTÃO ===
class Botao:
    def __init__(self, x, y, w, h, texto, cor):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.cor = cor
        self.fonte = pygame.font.SysFont("Arial", 24, bold=True)

    def desenhar(self, tela):
        cor_final = self.cor
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            cor_final = tuple(min(c + 40, 255) for c in self.cor)
        pygame.draw.rect(tela, cor_final, self.rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO, self.rect, 2, border_radius=10)
        txt = self.fonte.render(self.texto, True, BRANCO)
        tela.blit(txt, txt.get_rect(center=self.rect.center))

    def clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

# === AUXILIARES DE INTERFACE ===
def desenhar_texto(tela, texto, x, y, cor=BRANCO, tamanho=30, centralizado=False):
    fonte = pygame.font.SysFont("Arial", tamanho)
    img = fonte.render(str(texto), True, cor)
    pos = (x - img.get_width()//2, y) if centralizado else (x, y)
    tela.blit(img, pos)

def desenhar_barra_vida(tela, x, y, vida, vida_max, nome):
    desenhar_texto(tela, f"{nome}: {vida}/{vida_max}", x, y - 25, BRANCO, 18)
    pygame.draw.rect(tela, (50, 50, 50), (x, y, 200, 15))
    preenchimento = (max(0, vida) / vida_max) * 200
    pygame.draw.rect(tela, VERDE if vida > (vida_max * 0.3) else VERMELHO, (x, y, preenchimento, 15))

def desenhar_barra_mana(tela, x, y, mana, mana_max):
    desenhar_texto(tela, f"Mana: {mana}/{mana_max}", x, y - 20, (100, 100, 255), 16)
    pygame.draw.rect(tela, (50, 50, 50), (x, y, 200, 12))
    preenchimento = (max(0, mana) / mana_max) * 200
    pygame.draw.rect(tela, (0, 100, 255), (x, y, preenchimento, 12))

def processar_acao_local(opcao, jogador):
    if opcao == "Descansar":
        jogador.vida = jogador.vida_max
        jogador.mana = jogador.mana_max
        return "Você descansou e recuperou tudo!"
    return f"Selecionado: {opcao}"

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Python RPG Master")
    relogio = pygame.time.Clock()

    estado = "MENU_PRINCIPAL"
    jogador = None
    inimigo_atual = None
    log_combate = "Bem-vindo!"
    area_atual = "Vilarejo"

    # Botões Fixos
    btn_novo = Botao(300, 250, 200, 50, "Novo Jogo", VERDE)
    btn_carregar = Botao(300, 320, 200, 50, "Carregar", AZUL)
    btn_guerreiro = Botao(150, 300, 200, 60, "GUERREIRO", (150, 0, 0))
    btn_mago = Botao(450, 300, 200, 60, "MAGO", (0, 0, 150))

    while True:
        tela.fill(PRETO) # Limpa a tela no início de cada frame
        eventos = pygame.event.get()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- LÓGICA DE CLIQUE POR ESTADO ---
            if estado == "MENU_PRINCIPAL":
                if btn_novo.clicado(evento): estado = "SELECAO_SLOT_NOVO"
                if btn_carregar.clicado(evento): estado = "SELECAO_SLOT_CARREGAR"

            elif estado in ["SELECAO_SLOT_NOVO", "SELECAO_SLOT_CARREGAR"]:
                for i in range(1, 4):
                    rect_slot = pygame.Rect(250, 150 + (i*70), 300, 50)
                    if evento.type == pygame.MOUSEBUTTONDOWN and rect_slot.collidepoint(evento.pos):
                        slot_path = f"saves/save_slot_{i}.json"
                        definir_save(slot_path)
                        if "NOVO" in estado:
                            estado = "CRIACAO_PERSONAGEM"
                        elif os.path.exists(slot_path):
                            jogador, area_atual, _ = carregar_jogo()
                            estado = "MAPA"

            elif estado == "CRIACAO_PERSONAGEM":
                if btn_guerreiro.clicado(evento):
                    jogador = Guerreiro("Herói")
                    estado = "MAPA"
                if btn_mago.clicado(evento):
                    jogador = Mago("Herói")
                    estado = "MAPA"

            elif estado == "MAPA":
                opcoes = MAPA[area_atual]["opcoes"]
                destinos = MAPA[area_atual]["destinos"]
                for i, opcao in enumerate(opcoes):
                    rect_btn = pygame.Rect(LARGURA//2 - 150, 150 + (i*60), 300, 45)
                    if evento.type == pygame.MOUSEBUTTONDOWN and rect_btn.collidepoint(evento.pos):
                        if destinos[i]:
                            area_atual = destinos[i]
                        elif "Explorar" in opcao or "Enfrentar" in opcao:
                            inimigo_atual = inimigo_aleatorio(area_atual)
                            estado = "BATALHA"
                        elif "Salvar" in opcao:
                            salvar_jogo(jogador, area_atual)
                        else:
                            log_combate = processar_acao_local(opcao, jogador)

            elif estado == "BATALHA":
                for i in range(4):
                    rect_acao = pygame.Rect(40 + (i*185), 480, 175, 70)
                    if evento.type == pygame.MOUSEBUTTONDOWN and rect_acao.collidepoint(evento.pos):
                        if i == 0: # Atacar
                            dano = jogador.ataque_total()
                            inimigo_atual.vida -= dano
                            if inimigo_atual.vida <= 0:
                                jogador.ganhar_xp(getattr(inimigo_atual, 'xp_drop', 20))
                                estado = "MAPA"
                                log_combate = "Vitória!"
                            else:
                                dano_i = max(1, inimigo_atual.ataque - jogador.defesa_total())
                                jogador.vida -= dano_i
                                log_combate = f"Dano: {dano} | Recebeu: {dano_i}"

        # === DESENHO POR ESTADO ===
        if estado == "MENU_PRINCIPAL":
            desenhar_texto(tela, "PYTHON QUEST RPG", LARGURA//2, 100, VERDE, 60, True)
            btn_novo.desenhar(tela)
            btn_carregar.desenhar(tela)

        elif "SELECAO_SLOT" in estado:
            desenhar_texto(tela, "Selecione o Slot", LARGURA//2, 50, BRANCO, 40, True)
            for i in range(1, 4):
                rect = pygame.Rect(250, 150 + (i*70), 300, 50)
                existe = os.path.exists(f"saves/save_slot_{i}.json")
                pygame.draw.rect(tela, AZUL if existe else CINZA, rect, border_radius=5)
                desenhar_texto(tela, f"Slot {i} - {'Ocupado' if existe else 'Vazio'}", 400, 160 + (i*70), BRANCO, 24, True)

        elif estado == "CRIACAO_PERSONAGEM":
            desenhar_texto(tela, "Escolha sua Classe", LARGURA//2, 150, BRANCO, 45, True)
            btn_guerreiro.desenhar(tela)
            btn_mago.desenhar(tela)

        elif estado == "MAPA":
            desenhar_texto(tela, f"Área: {area_atual}", LARGURA//2, 30, VERDE, 30, True)
            desenhar_texto(tela, MAPA[area_atual]["descricao"], LARGURA//2, 70, BRANCO, 18, True)
            for i, opcao in enumerate(MAPA[area_atual]["opcoes"]):
                cor = AZUL if MAPA[area_atual]["destinos"][i] else CINZA
                Botao(LARGURA//2 - 150, 150 + (i*60), 300, 45, opcao, cor).desenhar(tela)
            desenhar_barra_vida(tela, 30, 540, jogador.vida, jogador.vida_max, jogador.nome)
            desenhar_texto(tela, log_combate, LARGURA//2, 450, OURO, 20, True)

        elif estado == "BATALHA":
            desenhar_barra_vida(tela, 20, 40, jogador.vida, jogador.vida_max, jogador.nome)
            desenhar_barra_mana(tela, 20, 90, jogador.mana, jogador.mana_max)
            desenhar_barra_vida(tela, 550, 40, inimigo_atual.vida, inimigo_atual.vida_max, inimigo_atual.nome)
            pygame.draw.circle(tela, AZUL, (200, 300), 50)
            pygame.draw.rect(tela, VERMELHO, (550, 250, 100, 100))
            acoes = ["ATACAR", "MAGIA", "DEFENDER", "ITENS"]
            cores = [VERMELHO, ROXO, AZUL, CINZA]
            for i, texto in enumerate(acoes):
                Botao(40 + (i*185), 480, 175, 70, texto, cores[i]).desenhar(tela)

        pygame.display.flip()
        relogio.tick(FPS)

if __name__ == "__main__":
    main()