import pygame
from pygame.locals import *

# CONSTANTES DE CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)

# CONSTANTES DE DIMENSÕES
largura = 800
altura= 600

class Interface:
    """Classe responsável por toda a interface gráfica do jogo"""
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Damas')
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.logo = pygame.image.load("logo.png")

    def desenha_tabuleiro_e_pecas(self, jogo):
        """Desenha o tabuleiro e todas as peças"""
        # Desenhar tabuleiro
        matriz = []
        for i in range(8):
            if i % 2 == 0:
                matriz.append(['#','-','#','-','#','-','#','-'])
            else:
                matriz.append(['-','#','-','#','-','#','-', '#'])

        y = 0
        for l in range(len(matriz)):
            x = 0
            for c in range(len(matriz[l])):
                if matriz[l][c] == '#':
                    pygame.draw.rect(self.display, COR_TABULEIRO, (x, y, 75, 75))
                else:
                    pygame.draw.rect(self.display, BRANCO, (x, y, 75, 75))
                x += 75
            y += 75

        # Destacar célula selecionada e movimentos possíveis
        if jogo.cedula_selecionada:
            obrigatorios = jogo.todos_obrigatorios()
            movs = jogo.movimentos_possiveis(jogo.cedula_selecionada)

            if obrigatorios != {}:
                if (jogo.cedula_selecionada[0], jogo.cedula_selecionada[1]) not in obrigatorios:
                    x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                    y_vermelho = altura / 8 * jogo.cedula_selecionada[0]

                    pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                else:
                    if movs[0] == []:
                        x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                        y_vermelho = altura / 8 * jogo.cedula_selecionada[0]

                        pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                    else:
                        for i in range(len(movs[0])):
                            x_possivel = altura / 8 * movs[0][i][1]
                            y_possivel = altura / 8 * movs[0][i][0]

                            pygame.draw.rect(self.display, VERDE, (x_possivel, y_possivel, 75, 75))
            else:
                if jogo.pulando:
                    x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                    y_vermelho = altura / 8 * jogo.cedula_selecionada[0]
                    pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                else:
                    if movs[0] == []:
                        x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                        y_vermelho = altura / 8 * jogo.cedula_selecionada[0]
                        pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                    else:
                        for i in range(len(movs[0])):
                            x_possivel = altura / 8 * movs[0][i][1]
                            y_possivel = altura / 8 * movs[0][i][0]
                            pygame.draw.rect(self.display, VERDE, (x_possivel, y_possivel, 75, 75))

        # Desenhar peças
        matriz_jogo = jogo.get_matriz_para_desenho()
        for l in range(len(matriz_jogo)):
            for c in range(len(matriz_jogo[l])):
                elemento = matriz_jogo[l][c]
                if elemento != '-':
                    x = altura / 8 * c + altura / 16
                    y = altura / 8 * l + altura / 16

                    if elemento.lower() == 'x':
                        pygame.draw.circle(self.display, ROXO, (x, y), 20, 0)
                        if elemento == 'X':  # Dama
                            pygame.draw.circle(self.display, PRETO, (x, y), 10, 0)
                            pygame.draw.circle(self.display, AZUL, (x, y), 5, 0)
                    else:
                        pygame.draw.circle(self.display, LARANJA, (x, y), 20, 0)
                        if elemento == 'O':  # Dama
                            pygame.draw.circle(self.display, PRETO, (x, y), 10, 0)
                            pygame.draw.circle(self.display, AZUL, (x, y), 5, 0)

    def desenha_interface_jogo(self, jogo):
        """Desenha as informações da interface durante o jogo"""
        fonte = pygame.font.Font(None, 20)
        
        x = jogo.tabuleiro.contar_pecas('x')
        o = jogo.tabuleiro.contar_pecas('o')

        if jogo.status != 'Game Over':

            # Contador de peças
            surface_texto, rect_texto = self.text_objects("Roxo: " + str(12 - o), fonte, ROXO)
            rect_texto.center = (650, 30)
            self.display.blit(surface_texto, rect_texto)

            surface_texto, rect_texto = self.text_objects("Laranja: " + str(12 - x), fonte, LARANJA)
            rect_texto.center = (650, altura - 30)
            self.display.blit(surface_texto, rect_texto)

            # Indicador de turno
            if jogo.turno % 2 == 1:
                surface_texto, rect_texto = self.text_objects("Laranja é sua vez", fonte, LARANJA)
                rect_texto.center = (700, altura / 2)
                self.display.blit(surface_texto, rect_texto)
            else:
                surface_texto, rect_texto = self.text_objects("Roxo é sua vez", fonte, ROXO)
                rect_texto.center = (700, altura / 2)
                self.display.blit(surface_texto, rect_texto)
        else:
            surface_texto, rect_texto = self.text_objects("Game Over", fonte, AZUL)
            rect_texto.center = (700, altura / 3)
            self.display.blit(surface_texto, rect_texto)

    def tela_menu(self,  loop_jogo, regras, sair):
        """Desenha o menu principal"""
        self.display.fill(PRETO)

        logo_rect = self.logo.get_rect(center=(largura // 2, altura // 4))
        self.display.blit(self.logo, logo_rect)
        

        self.cria_botao("INICIAR",(largura - 650, altura / 2, 120, 60), BRANCO, AZUL, PRETO, loop_jogo)
        self.cria_botao("REGRAS",(largura - 450, altura / 2, 120, 60),BRANCO, AZUL, PRETO, regras)
        self.cria_botao("SAIR",(largura - 250, altura / 2, 120, 60), BRANCO, AZUL, PRETO, sair)

    def tela_regras(self):

        self.display.fill(PRETO)
    
        fonte = pygame.font.SysFont('comicsansms', 20)

        info1 = fonte.render('O jogo de damas é jogado em um tabuleiro de 64 casas, com 12 peças por jogador.', False, BRANCO)
        info2 = fonte.render('As peças movem-se na diagonal, uma casa por vez, sempre para frente.', False, BRANCO)
        info3 = fonte.render('Ao chegar à última linha, a peça vira dama e pode andar para trás também.', False, BRANCO)
        info4 = fonte.render('A dama se move na diagonal, para frente e para trás, por várias casas.', False, BRANCO)
        info5 = fonte.render('Capturas são obrigatórias. A peça salta sobre a do oponente para capturá-la.', False, BRANCO)
        info6 = fonte.render('É permitido fazer capturas múltiplas numa só jogada, se possível.', False, BRANCO)
        info7 = fonte.render('Peças não podem pular outras da mesma cor.', False, BRANCO)
        info8 = fonte.render('O jogo termina quando um jogador não tiver mais peças ou movimentos.', False, BRANCO)
        game1 = fonte.render('Clique em uma peça para ver seus movimentos válidos (marcados em verde).', False, VERDE)
        game2 = fonte.render('Se não houver destaque, é porque não há jogadas ou não é seu turno.', False, BRANCO)
        voltar = fonte.render('Pressione ESC para voltar ao menu.', False, BRANCO)

        self.display.blit(info1, (10, 65))
        self.display.blit(info2, (10, 90))
        self.display.blit(info3, (10, 120))
        self.display.blit(info4, (10, 150))
        self.display.blit(info5, (10, 180))
        self.display.blit(info6, (10, 210))
        self.display.blit(info7, (10, 240))
        self.display.blit(info8, (10, 270))
        self.display.blit(game1, (10, 300))
        self.display.blit(game2, (10, 330))
        self.display.blit(voltar, (10, 550))


    def tela_vencedor_display(self, vencedor):
        """Exibe a tela do vencedor"""
        self.display.fill(PRETO)
        fonte = pygame.font.SysFont('comicsansms', 50)

        surface_texto, rect_texto = None, None

        if vencedor == "Empate":
            surface_texto, rect_texto = self.text_objects("EMPATE!", fonte, BRANCO)
        elif vencedor == "x":
            surface_texto, rect_texto = self.text_objects("VITORIA DO ROXO", fonte, ROXO)
        elif vencedor == "o":
            surface_texto, rect_texto = self.text_objects("VITORIA DO LARANJA", fonte, LARANJA)

        rect_texto.center = ((largura / 2), altura / 3)
        self.display.blit(surface_texto, rect_texto)

        fonte = pygame.font.Font(None, 30)
        voltar = fonte.render('Pressione ESC para voltar ao menu.', False, BRANCO)
        self.display.blit(voltar, (25, 550))

    def text_objects(self, text, font, color):
        """Cria objetos de texto para exibição"""
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def cria_botao(self, msg, sqr, cor1, cor2, cor_texto, acao=None):
        """Cria um botão interativo"""
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        if sqr[0] + sqr[2] > mouse[0] > sqr[0] and sqr[1] + sqr[3] > mouse[1] > sqr[1]:
            pygame.draw.rect(self.display, cor2, sqr)
            if clique[0] == 1 and acao != None:
                acao()
        else:
            pygame.draw.rect(self.display, cor1, sqr)

        fontePequena = pygame.font.SysFont('comicsansms', 20)
        surface_texto, rect_texto = self.text_objects(msg, fontePequena, cor_texto)
        rect_texto.center = (sqr[0] + 60, sqr[1] + 20)
        self.display.blit(surface_texto, rect_texto)

    def atualizar_display(self):
        """Atualiza a tela"""
        pygame.display.update()

    def tick(self, fps=60):
        """Controla o FPS"""
        self.clock.tick(fps)

    def limpar_tela(self, cor=PRETO):
        """Limpa a tela com uma cor"""
        self.display.fill(cor)