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
    nick1, nick2 = interface.tela_nomes()
    loop_jogo(nick1, nick2)


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
