import random
import pprint

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
        self.rows = 22
        self.cols = 12
        self.game_map = None
        self.tetromino = None

        self.update_map = self.iter_tetromino_area(self.update_map_action)
        self.collide_detect = \
            self.iter_tetromino_area(self.collide_detect_action)

        self.game_over = False

    def get_tetromino_area(self):
        window_x0 = self.tetromino.pos_x
        window_y0 = self.tetromino.pos_y
        tetromino_len = self.tetromino.length
        window_x1 = window_x0 + tetromino_len
        window_y1 = window_y0 - tetromino_len
        if window_y1 < 0:
            window_y1 = -1
        return window_x0, window_x1, window_y0, window_y1

    def iter_tetromino_area(self, action):
        def func():
            window_x0, window_x1, window_y0, window_y1 = self.get_tetromino_area()
            print(window_x0, window_x1, window_y0, window_y1)
            tetromino_x = 0
            for i in range(window_x0, window_x1):
                tetromino_y = self.tetromino.length - 1
                for j in range(window_y0, window_y1, -1):
                    if action(j, i, tetromino_y, tetromino_x):
                        return True
                    tetromino_y -= 1
                tetromino_x += 1
            return False

        return func

    def update_map_action(self, j, i, tetromino_y, tetromino_x):
        self.game_map[j][i] += \
            self.tetromino.tetromino[tetromino_y][tetromino_x]

    def collide_detect_action(self, j, i, tetromino_y, tetromino_x):
        if (self.game_map[j][i] +
                self.tetromino.tetromino[tetromino_y][tetromino_x]) > 1:
            return True

    def move_down(self):
        self.tetromino.pos_y += 1
        if self.collide_detect():
            self.tetromino.pos_y -= 1
            self.update_map()
            self.add_tetromino()
            self.print_game()

    def move_right(self):
        self.tetromino.pos_x += 1
        if self.collide_detect():
            self.tetromino.pos_x -= 1

    def move_left(self):
        self.tetromino.pos_x -= 1
        if self.collide_detect():
            self.tetromino.pos_x += 1

    def add_tetromino(self):
        self.tetromino = Tetromino(self.cols)
        if self.collide_detect():
            self.game_over = True

    def init_map(self):
        self.game_map = \
            [[0 for col in range(self.cols)] for row in range(self.rows)]
        # draw wall
        for i in range(self.rows):
            self.game_map[i][0] = 1
            self.game_map[i][-1] = 1
        for j in range(self.cols):
            self.game_map[-2][j] = 1
            self.game_map[-1][j] = 1

    def init_game(self):
        self.init_map()
        self.add_tetromino()

    def run(self):
        self.init_game()
        while not self.game_over:
            self.move_down()

    def print_game(self):
        pprint.pprint(self.game_map)


class Tetromino:
    def __init__(self, map_cols: int):
        self.tetromino_type = random.randint(0, len(tetrominos) - 1)
        self.orient = 0
        self.tetromino = tetrominos[self.tetromino_type][self.orient]
        self.length = len(self.tetromino)
        self.pos_x = random.randint(1, map_cols - self.length - 1)
        self.pos_y = 1

    def rotate(self):
        self.orient += 1
        self.tetromino = tetrominos[self.tetromino_type][self.orient]


game = GameMap()
game.run()
