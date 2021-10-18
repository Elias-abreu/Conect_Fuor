import numpy as np


class Heuristicas:
    def __init__(self):
        self.linhas = 6
        self.colunas = 7

    def iniciar_grade(self):
        grid = np.zeros((self.linhas, self.colunas))
        return grid

    def avaliar_sequencia(self,lista_sequencia, jogador):
        score = 0
        oponente = 2
        if jogador == 2:
            oponente = 1
        if lista_sequencia.count(jogador) == 4:
            score += 100
        elif lista_sequencia.count(jogador) == 3 and lista_sequencia.count(0) == 1:
            #print("Aqui 1")
            score += 5
        elif lista_sequencia.count(jogador) == 2 and lista_sequencia.count(0) == 2:
            #print("Aqui 2")
            score += 2
        if lista_sequencia.count(oponente) == 3 and lista_sequencia.count(0) == 1:
            score -= 4
        #elif lista_sequencia.count(oponente) == 2 and lista_sequencia.count(0) == 2:
            #score -= 2
        return score

    def avaliar_posicoes(self, grid, jogador):
        score = 0
        ## Score center column
        #center_array = [int(i) for i in list(grid[:, self.colunas // 2])]
        # print("Center")
        # print(center_array)
        #center_count = center_array.count(jogador)
        #score += center_count * 3

        #Avaliação Horizontal
        for l in range(self.linhas):
            linhas_array = [int(i) for i in list(grid[l, :])]
            for c in range(self.colunas - 3):
                #print("horizontal")
                lista_seq = linhas_array[c:c + 4]
                score += self.avaliar_sequencia(lista_seq, jogador)


        ##Avaliação Vertical
        for c in range(self.colunas):
            col_array = [int(i) for i in list(grid[:, c])]
            for r in range(self.linhas - 3):
                #print("Vertical")
                lista_seq = col_array[r:r + 4]
                score += self.avaliar_sequencia(lista_seq, jogador)

        #Avaliação  diagonal
        for r in range(self.linhas - 3):
            #print("Diagonal 1")
            for c in range(self.colunas - 3):
                lista_seq = [grid[r + i][c + i] for i in range(4)]
                score += self.avaliar_sequencia(lista_seq, jogador)

        #Avaliação  diagonal secundária
        for r in range(self.linhas - 3):
            for c in range(self.colunas - 3):
                #print("Diagonal 2")
                lista_seq = [grid[r + 3 - i][c + i] for i in range(4)]
                score += self.avaliar_sequencia(lista_seq, jogador)

        return score


if __name__ == '__main__':
    h = Heuristicas()
    grid = h.iniciar_grade()
    grid[0][0] = 1
    grid[0][1] = 2
    grid[0][2] = 2
    grid[0][3] = 2
    grid[0][4] = 1
    grid[0][5] = 0
    grid[0][6] = 0

    grid[1][0] = 1
    grid[1][1] = 2
    grid[1][2] = 2
    grid[1][3] = 2
    grid[1][4] = 0
    grid[1][5] = 0
    grid[1][6] = 0

    grid[2][0] = 0
    grid[2][1] = 0
    grid[2][2] = 0
    grid[2][3] = 0
    grid[2][4] = 0
    grid[2][5] = 0
    grid[2][6] = 0
    print(grid)
    print(h.avaliar_posicoes(grid,1))
