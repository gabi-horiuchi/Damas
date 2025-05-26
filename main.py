import pygame
from game import Jogo
from interface import Interface, altura

def coluna_clicada(pos):
    """Calcula qual coluna foi clicada"""
    x = pos[0]
    for i in range(1, 8):
        if x < i * altura / 8:
            return i - 1
    return 7

def linha_clicada(pos):
    """Calcula qual linha foi clicada"""
    y = pos[1]
    for i in range(1, 8):
        if y < i * altura / 8:
            return i - 1
    return 7

def loop_jogo():
    """Loop principal do jogo de damas"""
    interface = Interface()
    jogo = Jogo()
    
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                jogo.avalia_clique(pygame.mouse.get_pos(), linha_clicada, coluna_clicada)

        interface.limpar_tela()
        interface.desenha_tabuleiro_e_pecas(jogo)
        interface.desenha_interface_jogo(jogo)

        vencedor = jogo.verifica_vencedor()
        if vencedor is not None:
            tela_vencedor(vencedor, interface)
            break

        interface.atualizar_display()
        interface.tick(60)

def regras():
    """Exibe a tela de regras"""
    interface = Interface()
    sair = False

    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                event.key == pygame.K_ESCAPE
                sair = True

        interface.tela_regras()
        interface.atualizar_display()
        interface.tick(60)

def tela_vencedor(vencedor, interface):
    """Exibe a tela do vencedor"""
    sair = False

    while not sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                event.key == pygame.K_ESCAPE
                sair = True

        interface.tela_vencedor_display(vencedor)
        interface.atualizar_display()
        interface.tick(60)

def sair():
    """Encerra o jogo"""
    pygame.quit()
    quit()

def menu_jogo():
    """Loop do menu principal"""
    interface = Interface()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        interface.tela_menu(loop_jogo, regras, sair)
        interface.atualizar_display()
        interface.tick(15)

def main():
    """Função principal - ponto de entrada do programa"""
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