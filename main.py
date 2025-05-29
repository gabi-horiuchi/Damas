import pygame
from game import Jogo
from interface import Interface, altura

def coluna_clicada(pos):
    x = pos[0]
    for i in range(1, 8):
        if x < i * altura / 8:
            return i - 1
    return 7

def linha_clicada(pos):
    y = pos[1]
    for i in range(1, 8):
        if y < i * altura / 8:
            return i - 1
    return 7

def loop_jogo(nick1="Player 1", nick2="Player 2"):
    interface = Interface()
    jogo = Jogo()
    jogo.jogador_x.nome = nick1
    jogo.jogador_o.nome = nick2

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                jogo.avalia_clique(pygame.mouse.get_pos(), linha_clicada, coluna_clicada)

        interface.limpar_tela()
        interface.desenha_tabuleiro_e_pecas(jogo)
        interface.desenha_interface_jogo(jogo)

        vencedor = jogo.verifica_vencedor()
        if vencedor is not None:
            tela_vencedor(vencedor, interface, jogo)
            return

        interface.atualizar_display()
        interface.tick(60)

def iniciar_jogo_com_nomes(interface):
    nick1, nick2 = tela_nomes(interface)
    loop_jogo(nick1, nick2)

def tela_nomes(interface):
    nick1 = ""
    nick2 = ""
    fonte = pygame.font.Font(None, 36)
    ativo1 = ativo2 = False

    input_box1 = pygame.Rect(250, 200, 300, 50)
    input_box2 = pygame.Rect(250, 300, 300, 50)

    cor_inativo = (180, 180, 180)
    cor_ativo = (0, 255, 0)
    fundo_input = (30, 30, 30)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                ativo1 = input_box1.collidepoint(evento.pos)
                ativo2 = input_box2.collidepoint(evento.pos) and not ativo1
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nick1 and nick2:
                    return nick1, nick2
                if ativo1:
                    if evento.key == pygame.K_BACKSPACE:
                        nick1 = nick1[:-1]
                    elif len(nick1) < 6 and evento.unicode.isprintable():
                        nick1 += evento.unicode
                elif ativo2:
                    if evento.key == pygame.K_BACKSPACE:
                        nick2 = nick2[:-1]
                    elif len(nick2) < 6 and evento.unicode.isprintable():
                        nick2 += evento.unicode


        interface.limpar_tela()

        # Estilos para caixas
        pygame.draw.rect(interface.display, fundo_input, input_box1, border_radius=8)
        pygame.draw.rect(interface.display, cor_ativo if ativo1 else cor_inativo, input_box1, 2, border_radius=8)

        pygame.draw.rect(interface.display, fundo_input, input_box2, border_radius=8)
        pygame.draw.rect(interface.display, cor_ativo if ativo2 else cor_inativo, input_box2, 2, border_radius=8)

        # Renderizar textos
        txt1 = nick1 if nick1 else "Nick Player 1"
        txt2 = nick2 if nick2 else "Nick Player 2"
        cor_txt1 = (255, 255, 255) if nick1 else (150, 150, 150)
        cor_txt2 = (255, 255, 255) if nick2 else (150, 150, 150)

        surface1 = fonte.render(txt1, True, cor_txt1)
        surface2 = fonte.render(txt2, True, cor_txt2)

        interface.display.blit(surface1, (input_box1.x + 10, input_box1.y + 10))
        interface.display.blit(surface2, (input_box2.x + 10, input_box2.y + 10))

        # Botão de instrução
        info = fonte.render("Pressione ENTER para começar", True, (0, 255, 0))
        interface.display.blit(info, (250, 400))

        info = fonte.render("Escolha seu Nick (max 6 letras)", True, (255,255,255))
        interface.display.blit(info, (250, 100))

        interface.atualizar_display()
        interface.tick(30)


def regras():
    interface = Interface()
    sair = False

    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sair = True

        interface.tela_regras()
        interface.atualizar_display()
        interface.tick(60)

def tela_vencedor(vencedor, interface):
    sair = False

    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sair = True

        interface.tela_vencedor_display(vencedor)
        interface.atualizar_display()
        interface.tick(60)

def sair():
    pygame.quit()
    quit()

def menu_jogo():
    interface = Interface()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        interface.tela_menu(lambda: iniciar_jogo_com_nomes(interface), regras, sair)
        interface.atualizar_display()
        interface.tick(15)

def main():
    try:
        menu_jogo()
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        print("Obrigado por jogar!")

if __name__ == "__main__":
    main()
