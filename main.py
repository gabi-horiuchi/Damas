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
    jogo.jogador_o.nome = nick1
    jogo.jogador_x.nome = nick2

    sair_loop = False
    while not sair_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair_loop = True
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

    input_box1 = pygame.Rect(200, 200, 300, 50)
    input_box2 = pygame.Rect(200, 300, 300, 50)

    cor_inativo = (180, 180, 180)
    cor_ativo = (0, 255, 0)
    fundo_input = (30, 30, 30)

    sair_input = False
    while not sair_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ativo1 = input_box1.collidepoint(event.pos)
                ativo2 = input_box2.collidepoint(event.pos) and not ativo1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nick1 and nick2:
                    return nick1, nick2
                if ativo1:
                    if event.key == pygame.K_BACKSPACE:
                        nick1 = nick1[:-1]
                    elif len(nick1) < 6 and event.unicode.isprintable():
                        nick1 += event.unicode
                elif ativo2:
                    if event.key == pygame.K_BACKSPACE:
                        nick2 = nick2[:-1]
                    elif len(nick2) < 6 and event.unicode.isprintable():
                        nick2 += event.unicode

        interface.limpar_tela()
        pygame.draw.rect(interface.display, fundo_input, input_box1, border_radius=8)
        pygame.draw.rect(interface.display, cor_ativo if ativo1 else cor_inativo, input_box1, 2, border_radius=8)

        pygame.draw.rect(interface.display, fundo_input, input_box2, border_radius=8)
        pygame.draw.rect(interface.display, cor_ativo if ativo2 else cor_inativo, input_box2, 2, border_radius=8)

        txt1 = nick1 if nick1 else "Nick Player 1"
        txt2 = nick2 if nick2 else "Nick Player 2"
        cor_txt1 = (255, 255, 255) if nick1 else (150, 150, 150)
        cor_txt2 = (255, 255, 255) if nick2 else (150, 150, 150)

        surface1 = fonte.render(txt1, True, cor_txt1)
        surface2 = fonte.render(txt2, True, cor_txt2)

        interface.display.blit(surface1, (input_box1.x + 10, input_box1.y + 10))
        interface.display.blit(surface2, (input_box2.x + 10, input_box2.y + 10))

        info = fonte.render("Pressione ENTER para começar", True, (0, 255, 0))
        interface.display.blit(info, (200, 400))

        info = fonte.render("Escolha seu Nick (max 6 letras)", True, (255,255,255))
        interface.display.blit(info, (200, 100))

        interface.atualizar_display()
        interface.tick(30)

def regras():
    interface = Interface()
    sair_regras = False

    while not sair_regras:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair_regras = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sair_regras = True

        interface.tela_regras()
        interface.atualizar_display()
        interface.tick(60)

def tela_vencedor(vencedor, interface, jogo):
    sair_vencedor = False

    while not sair_vencedor:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair_vencedor = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sair_vencedor = True

        interface.tela_vencedor_display(vencedor, jogo)
        interface.atualizar_display()
        interface.tick(60)

def encerrar_jogo():
    pygame.quit()
    quit()

def menu_jogo():
    interface = Interface()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        interface.tela_menu(lambda: iniciar_jogo_com_nomes(interface), regras, encerrar_jogo)
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
