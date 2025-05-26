from obj import Tabuleiro, Jogador, Posicao

class Jogo:
    """Classe principal que gerencia a lógica do jogo de damas"""
    
    def __init__(self):
        self.status = 'Jogando'
        self.turno = 1
        self.jogadores = ('x', 'o')
        self.cedula_selecionada = None
        self.pulando = False
        self.tabuleiro = Tabuleiro()
        
        # Criar jogadores
        self.jogador_x = Jogador('x', 'Roxo', (128, 0, 128))
        self.jogador_o = Jogador('o', 'Laranja', (255, 165, 0))
    
    def get_matriz_para_desenho(self):
        """Retorna a matriz do tabuleiro para ser desenhada pela interface"""
        return self.tabuleiro.matriz
    
    def avalia_clique(self, pos, linha_clicada_func, coluna_clicada_func):
        """Avalia um clique do mouse e executa a ação correspondente"""
        turno = self.turno % 2
        if self.status == "Jogando":
            linha, coluna = linha_clicada_func(pos), coluna_clicada_func(pos)
            if self.cedula_selecionada:
                movimento = self.is_movimento_valido(self.jogadores[turno], self.cedula_selecionada, linha, coluna)
                if movimento[0]:
                    self.jogar(self.jogadores[turno], self.cedula_selecionada, linha, coluna, movimento[1])
                elif linha == self.cedula_selecionada[0] and coluna == self.cedula_selecionada[1]:
                    movs = self.movimento_obrigatorio(self.cedula_selecionada)
                    if movs[0] == []:
                        if self.pulando:
                            self.pulando = False
                            self.proximo_turno()
                    self.cedula_selecionada = None
            else:
                if self.tabuleiro.get_peca(linha, coluna).lower() == self.jogadores[turno]:
                    self.cedula_selecionada = [linha, coluna]

    def is_movimento_valido(self, jogador, localizacao_cedula, linha_destino, coluna_destino):
        """Verifica se um movimento é válido"""
        linha_originaria = localizacao_cedula[0]
        coluna_originaria = localizacao_cedula[1]

        obrigatorios = self.todos_obrigatorios()

        if obrigatorios != {}:
            if (linha_originaria, coluna_originaria) not in obrigatorios:
                return False, None
            elif [linha_destino, coluna_destino] not in obrigatorios[(linha_originaria, coluna_originaria)]:
                return False, None

        movimento, pulo = self.movimentos_possiveis(localizacao_cedula)

        if [linha_destino, coluna_destino] in movimento:
            if pulo:
                if len(pulo) == 1:
                    return True, pulo[0]
                else:
                    for i in range(len(pulo)):
                        if abs(pulo[i][0] - linha_destino) == 1 and abs(pulo[i][1] - coluna_destino) == 1:
                            return True, pulo[i]

            if self.pulando:
                return False, None

            return True, None

        return False, None

    def todos_obrigatorios(self):
        """Retorna todos os movimentos obrigatórios de um turno"""
        todos = {}

        for r in range(8):
            for c in range(8):
                ob, pulos = self.movimento_obrigatorio((r, c))
                if ob != []:
                    todos[(r, c)] = ob

        return todos

    def existe_possivel(self):
        """Verifica se existe algum movimento possível"""
        for l in range(8):
            for c in range(8):
                if self.movimentos_possiveis((l, c))[0]:
                    return True
        return False

    def movimento_obrigatorio(self, localizacao_cedula):
        """Retorna os movimentos obrigatórios de uma peça"""
        obrigatorios = []
        posicao_cedula_pulada = []

        l = localizacao_cedula[0]
        c = localizacao_cedula[1]

        jogador = self.jogadores[self.turno % 2]
        index = self.jogadores.index(jogador)

        array = [jogador.lower(), jogador.upper(), '-']

        peca_atual = self.tabuleiro.get_peca(l, c)
        
        if peca_atual.islower() and peca_atual == jogador and self.turno % 2 == index:
            # Movimentos para peças normais
            if l > 0:
                if c < 7:
                    peca_diagonal = self.tabuleiro.get_peca(l - 1, c + 1)
                    if peca_diagonal.lower() not in array:
                        l_x = l - 1
                        l_c = c + 1

                        if l_x - 1 >= 0 and l_c + 1 <= 7:
                            if self.tabuleiro.get_peca(l_x - 1, l_c + 1) == '-':
                                obrigatorios.append([l_x - 1, l_c + 1])
                                posicao_cedula_pulada.append((l_x, l_c))
                if c > 0:
                    peca_diagonal = self.tabuleiro.get_peca(l - 1, c - 1)
                    if peca_diagonal.lower() not in array:
                        l_x = l - 1
                        l_c = c - 1

                        if l_x - 1 >= 0 and l_c - 1 >= 0:
                            if self.tabuleiro.get_peca(l_x - 1, l_c - 1) == '-':
                                obrigatorios.append([l_x - 1, l_c - 1])
                                posicao_cedula_pulada.append((l_x, l_c))
            if l < 7:
                if c < 7:
                    peca_diagonal = self.tabuleiro.get_peca(l + 1, c + 1)
                    if peca_diagonal.lower() not in array:
                        l_x = l + 1
                        l_c = c + 1

                        if l_x + 1 <= 7 and l_c + 1 <= 7:
                            if self.tabuleiro.get_peca(l_x + 1, l_c + 1) == '-':
                                obrigatorios.append([l_x + 1, l_c + 1])
                                posicao_cedula_pulada.append((l_x, l_c))
                if c > 0:
                    peca_diagonal = self.tabuleiro.get_peca(l + 1, c - 1)
                    if peca_diagonal.lower() not in array:
                        l_x = l + 1
                        l_c = c - 1

                        if l_x + 1 <= 7 and l_c - 1 >= 0:
                            if self.tabuleiro.get_peca(l_x + 1, l_c - 1) == '-':
                                obrigatorios.append([l_x + 1, l_c - 1])
                                posicao_cedula_pulada.append((l_x, l_c))

        elif peca_atual.isupper() and peca_atual == jogador.upper() and self.turno % 2 == index:
            # Movimentos para damas
            if not self.pulando and (jogador.lower() == 'x' and l != 7) or (jogador.lower() == 'o' and l != 0):
                # Diagonal superior esquerda
                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha - 1 < 0 or conta_coluna - 1 < 0: 
                        break
                    else:
                        peca_diagonal = self.tabuleiro.get_peca(conta_linha - 1, conta_coluna - 1)
                        if peca_diagonal not in array:
                            l_x = conta_linha - 1
                            l_c = conta_coluna - 1

                            if l_x - 1 >= 0 and l_c - 1 >= 0:
                                if self.tabuleiro.get_peca(l_x - 1, l_c - 1) == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.tabuleiro.get_peca(l_x - 1, l_c - 1) == '-':
                                                obrigatorios.append([l_x - 1, l_c - 1])
                                            else:
                                                break
                                        l_x -= 1
                                        l_c -= 1
                            break
                    conta_linha -= 1
                    conta_coluna -= 1

                # Diagonal superior direita
                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha - 1 < 0 or conta_coluna + 1 > 7: 
                        break
                    else:
                        peca_diagonal = self.tabuleiro.get_peca(conta_linha - 1, conta_coluna + 1)
                        if peca_diagonal not in array:
                            l_x = conta_linha - 1
                            l_c = conta_coluna + 1

                            if l_x - 1 >= 0 and l_c + 1 <= 7:
                                if self.tabuleiro.get_peca(l_x - 1, l_c + 1) == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x - 1 < 0 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.tabuleiro.get_peca(l_x - 1, l_c + 1) == '-':
                                                obrigatorios.append([l_x - 1, l_c + 1])
                                            else:
                                                break
                                        l_x -= 1
                                        l_c += 1
                            break
                    conta_linha -= 1
                    conta_coluna += 1

                # Diagonal inferior direita
                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha + 1 > 7 or conta_coluna + 1 > 7: 
                        break
                    else:
                        peca_diagonal = self.tabuleiro.get_peca(conta_linha + 1, conta_coluna + 1)
                        if peca_diagonal not in array:
                            l_x = conta_linha + 1
                            l_c = conta_coluna + 1

                            if l_x + 1 <= 7 and l_c + 1 <= 7:
                                if self.tabuleiro.get_peca(l_x + 1, l_c + 1) == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c + 1 > 7:
                                            break
                                        else:
                                            if self.tabuleiro.get_peca(l_x + 1, l_c + 1) == '-':
                                                obrigatorios.append([l_x + 1, l_c + 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c += 1
                            break
                    conta_linha += 1
                    conta_coluna += 1

                # Diagonal inferior esquerda
                conta_linha = l
                conta_coluna = c
                while True:
                    if conta_linha + 1 > 7 or conta_coluna - 1 < 0: 
                        break
                    else:
                        peca_diagonal = self.tabuleiro.get_peca(conta_linha + 1, conta_coluna - 1)
                        if peca_diagonal not in array:
                            l_x = conta_linha + 1
                            l_c = conta_coluna - 1

                            if l_x + 1 <= 7 and l_c - 1 >= 0:
                                if self.tabuleiro.get_peca(l_x + 1, l_c - 1) == '-':
                                    posicao_cedula_pulada.append((l_x, l_c))
                                    while True:
                                        if l_x + 1 > 7 or l_c - 1 < 0:
                                            break
                                        else:
                                            if self.tabuleiro.get_peca(l_x + 1, l_c - 1) == '-':
                                                obrigatorios.append([l_x + 1, l_c - 1])
                                            else:
                                                break
                                        l_x += 1
                                        l_c -= 1
                            break
                    conta_linha += 1
                    conta_coluna -= 1

        return obrigatorios, posicao_cedula_pulada

    def movimentos_possiveis(self, localizacao_cedula):
        """Mostra os movimentos possíveis de uma peça selecionada"""
        movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula)

        if movimentos == []:
            linha_atual = localizacao_cedula[0]
            coluna_atual = localizacao_cedula[1]

            peca_atual = self.tabuleiro.get_peca(linha_atual, coluna_atual)

            if peca_atual.islower():
                if peca_atual == 'o':
                    if linha_atual > 0:
                        if coluna_atual < 7:
                            if self.tabuleiro.get_peca(linha_atual - 1, coluna_atual + 1) == '-':
                                movimentos.append([linha_atual - 1, coluna_atual + 1])
                        if coluna_atual > 0:
                            if self.tabuleiro.get_peca(linha_atual - 1, coluna_atual - 1) == '-':
                                movimentos.append([linha_atual - 1, coluna_atual - 1])
                
                elif peca_atual == 'x':
                    if linha_atual < 7:
                        if coluna_atual < 7:
                            if self.tabuleiro.get_peca(linha_atual + 1, coluna_atual + 1) == '-':
                                movimentos.append([linha_atual + 1, coluna_atual + 1])
                        if coluna_atual > 0:
                            if self.tabuleiro.get_peca(linha_atual + 1, coluna_atual - 1) == '-':
                                movimentos.append([linha_atual + 1, coluna_atual - 1])
            elif peca_atual.isupper():
                # Movimentos da dama em todas as direções
                # Diagonal superior esquerda
                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha - 1 < 0 or conta_coluna - 1 < 0: 
                        break
                    else:
                        if self.tabuleiro.get_peca(conta_linha - 1, conta_coluna - 1) == '-':
                            movimentos.append([conta_linha - 1, conta_coluna - 1])
                        else: 
                            break
                    conta_linha -= 1
                    conta_coluna -= 1

                # Diagonal superior direita
                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha - 1 < 0 or conta_coluna + 1 > 7: 
                        break
                    else:
                        if self.tabuleiro.get_peca(conta_linha - 1, conta_coluna + 1) == '-':
                            movimentos.append([conta_linha - 1, conta_coluna + 1])
                        else: 
                            break
                    conta_linha -= 1
                    conta_coluna += 1

                # Diagonal inferior direita
                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha + 1 > 7 or conta_coluna + 1 > 7: 
                        break
                    else:
                        if self.tabuleiro.get_peca(conta_linha + 1, conta_coluna + 1) == '-':
                            movimentos.append([conta_linha + 1, conta_coluna + 1])
                        else: 
                            break
                    conta_linha += 1
                    conta_coluna += 1

                # Diagonal inferior esquerda
                conta_linha = linha_atual
                conta_coluna = coluna_atual
                while True:
                    if conta_linha + 1 > 7 or conta_coluna - 1 < 0: 
                        break
                    else:
                        if self.tabuleiro.get_peca(conta_linha + 1, conta_coluna - 1) == '-':
                            movimentos.append([conta_linha + 1, conta_coluna - 1])
                        else: 
                            break
                    conta_linha += 1
                    conta_coluna -= 1
                
        return movimentos, pulos

    def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
        """Executa uma jogada"""
        linha_atual = localizacao_cedula[0]
        coluna_atual = localizacao_cedula[1]
        char = self.tabuleiro.get_peca(linha_atual, coluna_atual)

        self.tabuleiro.set_peca(linha_destino, coluna_destino, char)
        self.tabuleiro.set_peca(linha_atual, coluna_atual, '-')

        if pulo:
            self.pulando = True

        # Promover para dama se chegou na extremidade
        if (jogador == 'x' and linha_destino == 7) or (jogador == 'o' and linha_destino == 0):
            if not self.pulando:
                self.tabuleiro.set_peca(linha_destino, coluna_destino, char.upper())
            elif not self.movimentos_possiveis((linha_destino, coluna_destino))[0]:
                self.tabuleiro.set_peca(linha_destino, coluna_destino, char.upper())

        if pulo:
            self.tabuleiro.set_peca(pulo[0], pulo[1], '-')
            self.cedula_selecionada = [linha_destino, coluna_destino]
            self.pulando = True
        else:
            self.cedula_selecionada = None
            self.proximo_turno()
            
        vencedor = self.verifica_vencedor()
        if vencedor != None:
            self.status = 'Game Over'

    def proximo_turno(self):
        """Avança para o próximo turno"""
        self.turno += 1

    def verifica_vencedor(self):
        """Verifica se há um vencedor"""
        x = self.tabuleiro.contar_pecas('x')
        o = self.tabuleiro.contar_pecas('o')

        if x == 0:
            return 'o'

        if o == 0:
            return 'x'

        if x == 1 and o == 1:
            return 'Empate'

        if self.cedula_selecionada:
            if not self.movimentos_possiveis(self.cedula_selecionada)[0]:
                if x == 1 and self.turno % 2 == 0:
                    return 'o'
                if o == 1 and self.turno % 2 == 1:
                    return 'x'

        if not self.existe_possivel():
            return 'Empate'

        return None