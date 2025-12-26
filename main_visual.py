import pygame
import sys
import os

# Importações do seu projeto
from core.jogador import Guerreiro  
from persistence.save import definir_save, salvar_jogo
from systems.mapa import inimigo_aleatorio

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
CINZA = (100, 100, 100)

class Botao:
    def __init__(self, x, y, w, h, texto, cor):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.cor = cor
        self.fonte = pygame.font.SysFont("Arial", 24)

    def desenhar(self, tela):
        cor_final = self.cor
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            cor_final = tuple(min(c + 40, 255) for c in self.cor)
        
        pygame.draw.rect(tela, cor_final, self.rect, border_radius=8)
        txt = self.fonte.render(self.texto, True, BRANCO)
        tela.blit(txt, txt.get_rect(center=self.rect.center))

    def clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

def desenhar_barra_vida(tela, x, y, vida, vida_max, nome):
    fonte = pygame.font.SysFont("Arial", 18)
    txt = fonte.render(f"{nome}: {vida}/{vida_max}", True, BRANCO)
    tela.blit(txt, (x, y - 25))
    
    largura_barra = 200
    pygame.draw.rect(tela, (50, 50, 50), (x, y, largura_barra, 15)) 
    preenchimento = (max(0, vida) / vida_max) * largura_barra
    cor_barra = VERDE if vida > (vida_max * 0.3) else VERMELHO
    pygame.draw.rect(tela, cor_barra, (x, y, preenchimento, 15))

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("RPG Visual - Teste de Combate")
    relogio = pygame.time.Clock()

    # 1. Configurar Save e Jogador
    definir_save("saves/teste_pygame.json")
    jogador = Guerreiro("Herói Teste")
    area_atual = "Vilarejo"
    
    # 2. Variáveis de Estado
    estado = "VILAREJO"
    inimigo_atual = None
    log_combate = "Bem-vindo ao Vilarejo!"

    # 3. Criar Botões
    btn_explorar = Botao(300, 250, 200, 50, "Explorar", AZUL)
    btn_salvar = Botao(300, 320, 200, 50, "Salvar Jogo", VERDE)
    btn_atacar = Botao(150, 480, 200, 60, "ATACAR", VERMELHO)
    btn_fugir = Botao(450, 480, 200, 60, "FUGIR", CINZA)

    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if estado == "VILAREJO":
                if btn_explorar.clicado(evento):
                    inimigo_atual = inimigo_aleatorio("Floresta")
                    estado = "BATALHA"
                    log_combate = f"Um {inimigo_atual.nome} apareceu!"
                
                if btn_salvar.clicado(evento):
                    salvar_jogo(jogador, area_atual)
                    log_combate = "Jogo Salvo com Sucesso!"

            elif estado == "BATALHA":
                if btn_atacar.clicado(evento):
                    # --- TURNO DO JOGADOR ---
                    dano = jogador.ataque_total()
                    inimigo_atual.vida -= dano
                    log_combate = f"Causaste {dano} de dano!"

                    if inimigo_atual.vida <= 0:
                        # Nota: Verifica se no teu Inimigo.py os nomes são xp/ouro ou xp_drop/ouro_drop
                        xp_ganho = getattr(inimigo_atual, 'xp_drop', getattr(inimigo_atual, 'xp', 0))
                        ouro_ganho = getattr(inimigo_atual, 'ouro_drop', getattr(inimigo_atual, 'ouro', 0))
                        
                        jogador.ganhar_xp(xp_ganho)
                        jogador.ouro += ouro_ganho
                        estado = "VILAREJO"
                        log_combate = f"Vitória! Ganhaste {xp_ganho} XP."
                    else:
                        # --- TURNO DO INIMIGO ---
                        dano_inimigo = max(1, inimigo_atual.ataque - jogador.defesa_total())
                        jogador.vida -= dano_inimigo
                        log_combate += f" | Recebeste {dano_inimigo} de dano!"
                        
                        if jogador.vida <= 0:
                            print("MORRESTE! Fim de Jogo.")
                            pygame.quit()
                            sys.exit()

                if btn_fugir.clicado(evento):
                    estado = "VILAREJO"
                    log_combate = "Fugiste como um cobarde!"

        # === DESENHO ===
        tela.fill(PRETO)
        
        # UI Básica
        desenhar_barra_vida(tela, 30, 50, jogador.vida, jogador.vida_max, jogador.nome)
        fonte_info = pygame.font.SysFont("Arial", 20)
        txt_stats = fonte_info.render(f"Ouro: {jogador.ouro} | Nível: {jogador.nivel}", True, OURO)
        tela.blit(txt_stats, (30, 80))

        # Log centralizado
        txt_log = fonte_info.render(log_combate, True, BRANCO)
        tela.blit(txt_log, (LARGURA//2 - txt_log.get_width()//2, 400))

        if estado == "VILAREJO":
            btn_explorar.desenhar(tela)
            btn_salvar.desenhar(tela)
            
        elif estado == "BATALHA":
            # --- REPRESENTAÇÃO VISUAL DOS PERSONAGENS ---
            # Herói (Círculo Azul)
            pygame.draw.circle(tela, AZUL, (200, 300), 50)
            pygame.draw.rect(tela, BRANCO, (180, 270, 15, 15)) # "Olho" do herói
            
            # Inimigo (Quadrado Vermelho)
            pygame.draw.rect(tela, VERMELHO, (550, 250, 100, 100))
            pygame.draw.line(tela, BRANCO, (570, 280), (590, 280), 3) # "Olho" 1
            pygame.draw.line(tela, BRANCO, (610, 280), (630, 280), 3) # "Olho" 2
            
            # Barra de vida do Inimigo
            desenhar_barra_vida(tela, 550, 50, inimigo_atual.vida, inimigo_atual.vida_max, inimigo_atual.nome)
            
            # Botões
            btn_atacar.desenhar(tela)
            btn_fugir.desenhar(tela)

        pygame.display.flip()
        relogio.tick(FPS)

if __name__ == "__main__":
    main()