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


def get_tetromino_area(pos_x: int, pos_y: int, tetromino_len: int) -> list:
    window_x0 = pos_x
    window_y0 = pos_y
    window_x1 = window_x0 + tetromino_len
    window_y1 = window_y0 - tetromino_len
    if window_y1 < 0:
        window_y1 = -1
    return [window_x0, window_x1, window_y0, window_y1]


class Tetromino:
    def __init__(self, map_cols: int):
        self.tetromino_type = random.randint(0, len(tetrominos) - 1)
        self.type_variants = len(tetrominos[self.tetromino_type])
        self.orient = 0
        self.length = len(tetrominos[self.tetromino_type][self.orient])
        self.pos_x = random.randint(1, map_cols - self.length - 1)
        self.pos_y = 1
