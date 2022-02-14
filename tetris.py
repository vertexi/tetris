import random

tetromino_I_1 = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0]]
tetromino_I_2 = [[0, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 0, 0]]

tetromino_L_1 = [[0, 0, 0],
                 [1, 1, 1],
                 [1, 0, 0]]
tetromino_L_2 = [[1, 1, 0],
                 [0, 1, 0],
                 [0, 1, 0]]
tetromino_L_3 = [[0, 0, 1],
                 [1, 1, 1],
                 [0, 0, 0]]
tetromino_L_4 = [[0, 1, 0],
                 [0, 1, 0],
                 [0, 1, 1]]

tetromino_J_1 = [[0, 0, 0],
                 [1, 1, 1],
                 [0, 0, 1]]
tetromino_J_2 = [[0, 1, 0],
                 [0, 1, 0],
                 [1, 1, 0]]
tetromino_J_3 = [[1, 0, 0],
                 [1, 1, 1],
                 [0, 0, 0]]
tetromino_J_4 = [[0, 1, 1],
                 [0, 1, 0],
                 [0, 1, 0]]

tetromino_S_1 = [[0, 0, 0],
                 [0, 1, 1],
                 [1, 1, 0]]
tetromino_S_2 = [[1, 0, 0],
                 [1, 1, 0],
                 [0, 1, 0]]

tetromino_Z_1 = [[0, 0, 0],
                 [1, 1, 0],
                 [0, 1, 1]]
tetromino_Z_2 = [[0, 1, 0],
                 [1, 1, 0],
                 [1, 0, 0]]

tetromino_T_1 = [[0, 0, 0],
                 [1, 1, 1],
                 [0, 1, 0]]
tetromino_T_2 = [[0, 1, 0],
                 [1, 1, 0],
                 [0, 1, 0]]
tetromino_T_3 = [[0, 1, 0],
                 [1, 1, 1],
                 [0, 0, 0]]
tetromino_T_4 = [[0, 1, 0],
                 [0, 1, 1],
                 [0, 1, 0]]

tetromino_O = [[1, 1],
               [1, 1]]

tetromino_I = [tetromino_I_1, tetromino_I_2]
tetromino_L = [tetromino_L_1, tetromino_L_2, tetromino_L_3, tetromino_L_4]
tetromino_J = [tetromino_J_1, tetromino_J_2, tetromino_J_3, tetromino_J_4]
tetromino_S = [tetromino_S_1, tetromino_S_2]
tetromino_Z = [tetromino_Z_1, tetromino_Z_2]
tetromino_T = [tetromino_T_1, tetromino_T_2, tetromino_T_3, tetromino_T_4]
tetromino_O = [tetromino_O]

tetrominos = [tetromino_I, tetromino_L, tetromino_J, tetromino_S,
              tetromino_Z, tetromino_T, tetromino_O]


class GameMap:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.game_map = \
            [[0 for col in range(self.cols)] for row in range(self.rows)]


class Tetromino:
    def __init__(self):
        self.tetromino_type = random.randint(0, 7 - 1)
        self.orient = random.randint(1, 4)
        self.tetromino = None

    def shape(self):
        self.tetromino = tetrominos[self.orient]
