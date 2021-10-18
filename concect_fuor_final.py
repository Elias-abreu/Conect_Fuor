import numpy as np
import copy
import pygame
import pygame
import sys
import math
from jogo_conect4.heuristica import Heuristicas

global contador_no
# implementar tabuleiro cheio = ok
# implementar heurística = feito duas, melhorar a primeira

class Conect_fuor_Final:

    def __init__(self):
        self.linhas = 6
        self.colunas = 7

    def iniciar_grade(self):
        grid = np.zeros((self.linhas, self.colunas))
        return grid

    # Verifica quem ganhou
    def teste_terminal(self, grid, jogador):
        # Verificar mat em linha
        for l in range(self.linhas):
            for c in range(self.colunas - 3):
                if (grid[l][c] == jogador and grid[l][c + 1] == jogador and grid[l][
                    c + 2] == jogador and grid[l][c + 3] == jogador):
                    return True
        # Verificar mat em coluna
        for c in range(self.colunas):
            for l in range(self.linhas - 3):
                if (grid[l][c] == jogador and grid[l + 1][c] == jogador and grid[l + 2][
                    c] == jogador and grid[l + 3][c] == jogador):
                    return True

        # Verificar Diagonal principal
        for c in range(self.colunas - 3):
            for l in range(self.linhas - 3):
                if grid[l][c] == jogador and grid[l + 1][c + 1] == jogador and grid[l + 2][
                    c + 2] == jogador and grid[l + 3][c + 3] == jogador:
                    return True

        # Verificar Diagonal secundária
        for c in range(self.colunas - 3):
            for l in range(3, self.linhas):
                if grid[l][c] == jogador and grid[l - 1][c + 1] == jogador and grid[l - 2][
                    c + 2] == jogador and grid[l - 3][c + 3] == jogador:
                    return True
        # Falta verifiar empate
        return False

    # Retorna True se acabou ou False se não acabou
    def verifica_terminal(self, grid):
        if (self.teste_terminal(grid, 1)):
            return True
        elif self.teste_terminal(grid, 2):
            return True
        else:
            return False

    # Recebe a coluna que se deseja adiconar e pega a ultima linha livre, ou seja, igual a 0 da coluna passada por parâmetro
    def ver_linha(self, grid, coluna):
        total = 0
        while total < self.linhas:
            # print(total)
            if (grid[total][coluna] == 0):
                return total
            total += 1
        return "cheio"

    # Retorna uma lista de movimentos possíveis
    def movimentos_posiveis(self, grid):
        acoes = []
        for c in range(self.colunas):
            for l in range(self.linhas):
                if (grid[l][c] == 0):
                    acoes.append([l, c])
                    break
        return acoes

    # Para validar todos os moviemntos analisados
    def validar_movimento(self, grid, movimento):
        if grid[movimento[0]][movimento[1]] == 0:
            return True
        return False

    # Realiza a joga, usa o copy para não referenciar
    def fazer_jogada(self, grid, pos, jogador):
        grid_pos = copy.deepcopy(grid)
        if self.validar_movimento(grid_pos, pos):
            grid_pos[pos[0], pos[1]] = jogador
            return grid_pos
        print("Movimento Inválido!!")
        return grid_pos

    def melhor_jogada(self, grid, jogador_atual, heuristica):
        if jogador_atual == 1:
            j = 2
        else:
            j = 1
        movimentos_possiveis = self.movimentos_posiveis(grid)
        melhor = -math.inf
        melhor_jogada = []
        alpha = -math.inf
        beta = math.inf
        cont = 0
        for movimento in movimentos_possiveis:
            global contador_no
            contador_no = 0
            resultado = self.fazer_jogada(grid, movimento, jogador_atual)
            valor = self.alfabeta(resultado, j, 5, alpha, beta, heuristica)  # Trocar o jogador aqui
            #valor = self.alfabeta2(resultado, j, alpha, beta, heuristica)  # Trocar o jogador aqui
            #valor = self.minimax(resultado, j, 5, heuristica)
            cont +=contador_no
            if valor > melhor:
                melhor_jogada = movimento
                melhor = valor
        # print(self.validar_movimento(grid,melhor_jogada))
        print("Melhor Utilidade: ",melhor," NÓs: ",cont)
        if not melhor_jogada:
            print("Pau aqui")
            melhor_jogada = movimento
        return melhor_jogada

    def minimax(self, grid, jogador_atual, profundidade, heuristica):
        ver_terminal = self.verifica_terminal(grid)
        global contador_no
        if ver_terminal:
            if self.teste_terminal(grid, 1):
                return 10000
            elif self.teste_terminal(grid, 2):
                return -10000
            else:
                return 0
        elif profundidade == 0:
            he = Heuristicas()
            if heuristica == 1:
                return he.avaliar3(grid, jogador_atual)
            elif heuristica == 2:
                avaliacao = he.avaliar_posicoes(grid, jogador_atual)
                #print(avaliacao)
                return avaliacao
        # max = 1 e min = 2
        movimentos_possiveis = self.movimentos_posiveis(grid)
        # print(movimentos_possiveis)
        if jogador_atual == 1:
            melhor_max = -100
            for movimento in movimentos_possiveis:
                resultado = self.fazer_jogada(grid, movimento, jogador_atual)
                valor_resutado = self.minimax(resultado, 2, profundidade - 1, heuristica)
                contador_no += 1
                if valor_resutado > melhor_max:
                    melhor_max = valor_resutado
            return melhor_max
        elif jogador_atual == 2:
            melhor_min = 100
            for movimento in movimentos_possiveis:
                resultado = self.fazer_jogada(grid, movimento, jogador_atual)
                valor_resutado = self.minimax(resultado, 1, profundidade - 1, heuristica)
                contador_no += 1
                if valor_resutado < melhor_min:
                    melhor_min = valor_resutado
            return melhor_min

    def alfabeta(self, grid, jogador_atual, profundidade, alpha, beta, heuristica):
        ver_terminal = self.verifica_terminal(grid)
        global contador_no
        if ver_terminal:
            if self.teste_terminal(grid, 1):
                return 10000
            elif self.teste_terminal(grid, 2):
                return -10000
            else:
                return 0
        elif profundidade == 0:
            he = Heuristicas()
            if heuristica == 1:
                return he.avaliar3(grid, jogador_atual)
            elif heuristica == 2:
                avaliacao = he.avaliar_posicoes(grid, jogador_atual)
                #print(avaliacao)
                return avaliacao
        # max = 1 e min = 2
        movimentos_possiveis = self.movimentos_posiveis(grid)
        # print(movimentos_possiveis)
        if jogador_atual == 1:
            melhor_max = -math.inf
            for movimento in movimentos_possiveis:
                resultado = self.fazer_jogada(grid, movimento, jogador_atual)
                valor_resutado = self.alfabeta(resultado, 2, profundidade - 1, alpha, beta, heuristica)
                if valor_resutado > melhor_max:
                    melhor_max = valor_resutado
                alpha = max(alpha, melhor_max)
                contador_no +=1
                if melhor_max >= beta:
                    break
            return melhor_max
        elif jogador_atual == 2:
            melhor_min = math.inf
            for movimento in movimentos_possiveis:
                resultado = self.fazer_jogada(grid, movimento, jogador_atual)
                valor_resutado = self.alfabeta(resultado, 1, profundidade - 1, alpha, beta, heuristica)
                if valor_resutado < melhor_min:
                    melhor_min = valor_resutado
                beta = min(beta, melhor_min)
                contador_no += 1
                if melhor_min <= alpha:
                    break
            return melhor_min

    def alfabeta2(self, grid, jogador_atual, alpha, beta, heuristica):
        ver_terminal = self.verifica_terminal(grid)
        if ver_terminal:
            if self.teste_terminal(grid, 1):
                return 10000
            elif self.teste_terminal(grid, 2):
                return -10000
            else:
                return 0
        # max = 1 e min = 2
        movimentos_possiveis = self.movimentos_posiveis(grid)
        # print(movimentos_possiveis)
        if jogador_atual == 1:
            melhor_max = -math.inf
            for movimento in movimentos_possiveis:
                resultado = self.fazer_jogada(grid, movimento, jogador_atual)
                valor_resutado = self.alfabeta2(resultado, 2 - 1, alpha, beta, heuristica)
                if valor_resutado > melhor_max:
                    melhor_max = valor_resutado
                alpha = max(alpha, melhor_max)
                if melhor_max >= beta:
                    break
            return melhor_max
        elif jogador_atual == 2:
            melhor_min = math.inf
            for movimento in movimentos_possiveis:
                resultado = self.fazer_jogada(grid, movimento, jogador_atual)
                valor_resutado = self.alfabeta2(resultado, 1, alpha, beta, heuristica)
                if valor_resutado < melhor_min:
                    melhor_min = valor_resutado
                beta = min(beta, melhor_min)
                if melhor_min <= alpha:
                    break
            return melhor_min

    def principal(self, jogador):
        grid = self.iniciar_grade()
        # Configurações do desing
        SQUARESIZE = 90
        width = self.colunas * SQUARESIZE
        height = (self.linhas + 1) * SQUARESIZE
        size = (width, height)
        RADIUS = int(SQUARESIZE / 2 - 5)
        screen = pygame.display.set_mode(size)
        myfont = pygame.font.SysFont("monospace", 50)
        tempo = 20000
        self.draw_board(grid)
        pygame.display.update()

        gameover = False
        while not gameover:
            for event in pygame.event.get():
                # Se clicar para fechar
                if event.type == pygame.QUIT:
                    gameover = True
                    tempo = 0
                    break

                # Verificar se empatou
                if not self.movimentos_posiveis(grid):
                    gameover = True
                    label = myfont.render("Empate", 1, (255, 255, 255))
                    screen.blit(label, (50, 10))
                    print(grid)

                # Desenha o circlo na barra superior (Desenha na posição do mouse)
                # Para o jogador 1 e para o Jogador 2
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if jogador == 1:
                        pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                    elif jogador == 2:
                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    coluna = int(math.floor(posx / SQUARESIZE))
                    linha = self.ver_linha(grid, coluna)
                    if (linha != "cheio"):
                        grid[linha][coluna] = jogador
                        gameover = c.teste_terminal(grid, jogador)
                        self.draw_board(grid)
                        if gameover == True:
                            gameover = True
                            print("Você Ganhou")
                            label = myfont.render("Você Ganhou", 1, (255, 255, 255))
                            screen.blit(label, (50, 10))
                            print(grid)
                        elif (jogador == 2):
                            jogador = 1
                        elif jogador == 1:
                            jogador = 2

                pygame.display.flip()
            if gameover:
                pygame.time.wait(tempo)

    def principal_d(self, jogador,heuristica):
        grid = self.iniciar_grade()
        # Configurações do desing
        SQUARESIZE = 90
        width = self.colunas * SQUARESIZE
        height = (self.linhas + 1) * SQUARESIZE
        size = (width, height)
        RADIUS = int(SQUARESIZE / 2 - 5)
        screen = pygame.display.set_mode(size)
        myfont = pygame.font.SysFont("monospace", 50)
        tempo = 20000
        self.draw_board(grid)
        pygame.display.update()

        gameover = False
        while not gameover:
            for event in pygame.event.get():
                # Se clicar para fechar
                if event.type == pygame.QUIT:
                    gameover = True
                    tempo = 0
                    break

                # Verificar se empatou
                if not self.movimentos_posiveis(grid):
                    gameover = True
                    label = myfont.render("Empate", 1, (255, 255, 255))
                    screen.blit(label, (50, 10))
                    print(grid)

                # Desenha o circlo na barra superior (Desenha na posição do mouse)
                # Para o jogador 1 e para o Jogador 2
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if jogador == 1:
                        pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                    elif jogador == 2:
                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if jogador == 2:
                    # Se o evento for de soltar
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        posx = event.pos[0]
                        coluna = int(math.floor(posx / SQUARESIZE))
                        linha = self.ver_linha(grid, coluna)
                        if (linha != "cheio"):
                            grid[linha][coluna] = jogador
                            gameover = c.teste_terminal(grid, jogador)
                            self.draw_board(grid)
                            if gameover == True:
                                gameover = True
                                print("Você Ganhou")
                                label = myfont.render("Você Ganhou", 1, (255, 255, 255))
                                screen.blit(label, (50, 10))
                                print(grid)
                            elif (jogador == 2):
                                jogador = 1

                    pygame.display.flip()
            if jogador == 1:
                melhor_jogada = self.melhor_jogada(grid, jogador, heuristica)
                grid[melhor_jogada[0]][melhor_jogada[1]] = 1
                gameover = c.teste_terminal(grid, jogador)
                self.draw_board(grid)
                if gameover == True:
                    print("IA venceu")
                    label = myfont.render("IA venceu ", 1, (255, 255, 255))
                    screen.blit(label, (50, 10))
                    print(grid)
                elif (jogador == 1):
                    jogador = 2
                elif (jogador == 2):
                    jogador = 1
            pygame.display.flip()
            if gameover:
                pygame.time.wait(tempo)

    def principal_2IA(self, jogador):
        grid = self.iniciar_grade()
        # Configurações do desing
        SQUARESIZE = 90
        width = self.colunas * SQUARESIZE
        height = (self.linhas + 1) * SQUARESIZE
        size = (width, height)
        RADIUS = int(SQUARESIZE / 2 - 5)
        screen = pygame.display.set_mode(size)
        myfont = pygame.font.SysFont("monospace", 50)
        tempo = 20000
        self.draw_board(grid)
        pygame.display.update()

        gameover = False
        while not gameover:
            for event in pygame.event.get():
                # Se clicar para fechar
                if event.type == pygame.QUIT:
                    gameover = True
                    tempo = 0
                    break

                # Verificar se empatou
                if not self.movimentos_posiveis(grid):
                    gameover = True
                    label = myfont.render("Empate", 1, (255, 255, 255))
                    screen.blit(label, (50, 10))
                    print(grid)

                # Desenha o circlo na barra superior (Desenha na posição do mouse)
                # Para o jogador 1 e para o Jogador 2
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if jogador == 1:
                        pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                    elif jogador == 2:
                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if jogador == 2:
                    melhor_jogada = self.melhor_jogada(grid, jogador, 2)
                    grid[melhor_jogada[0]][melhor_jogada[1]] = 2
                    gameover = c.teste_terminal(grid, jogador)
                    self.draw_board(grid)
                    if gameover == True:
                        print("IA 1 venceu")
                        label = myfont.render("IA 1 venceu ", 1, (255, 255, 255))
                        screen.blit(label, (50, 10))
                        print(grid)
                    elif (jogador == 2):
                        jogador = 1
                    elif (jogador == 1):
                        jogador = 2

                    pygame.display.flip()
            if jogador == 1:
                melhor_jogada = self.melhor_jogada(grid, jogador, 2)
                grid[melhor_jogada[0]][melhor_jogada[1]] = 1
                gameover = c.teste_terminal(grid, jogador)
                self.draw_board(grid)
                if gameover == True:
                    print("IA 2 venceu")
                    label = myfont.render("IA 2 venceu ", 1, (255, 255, 255))
                    screen.blit(label, (50, 10))
                    print(grid)
                elif (jogador == 1):
                    jogador = 2
                elif (jogador == 2):
                    jogador = 1
            pygame.display.flip()
            if gameover:
                pygame.time.wait(tempo)

    # Reponsável por desenhar o jogo na tela
    def draw_board(self, grid):
        BLUE = (255, 255, 255)  # Cor da grade
        BLACK = (0, 0, 0)  # Cor de fundo
        RED = (255, 0, 0)  # Cor da primeira bolinha
        YELLOW = (255, 255, 0)  # Cor da segunda bolinha
        SQUARESIZE = 90
        width = self.colunas * SQUARESIZE
        height = (self.linhas + 1) * SQUARESIZE
        size = (width, height)
        RADIUS = int(SQUARESIZE / 2 - 5)
        screen = pygame.display.set_mode(size)
        PLAYER_PIECE = 1  # controlar quem jogou com 1
        AI_PIECE = 2  # Controlar quem jogou com 2

        for c in range(self.colunas):
            for r in range(self.linhas):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(self.colunas):
            for r in range(self.linhas):
                if grid[r][c] == PLAYER_PIECE:
                    pygame.draw.circle(screen, RED, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif grid[r][c] == AI_PIECE:
                    pygame.draw.circle(screen, YELLOW, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)


if __name__ == '__main__':
    pygame.init()
    c = Conect_fuor_Final()
    grid = c.iniciar_grade()
    '''
    grid[0][1] = 1
    grid[0][2] = 1
    grid[0][3] = 1
    grid[0][4] = 1
    print(c.verifica_terminal(grid))
    '''
    #heuristica 1 será pevando em consideração apenas conexão de três;
    heuristica = 2 #Leva em consideração vários fatores
    #Digite 1 para a IA começar e 2 para o oponente
    c.principal_d(2,heuristica)
