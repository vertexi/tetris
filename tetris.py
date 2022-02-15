import graphic
import utime
from tetromino import get_tetromino_area, Tetromino, tetrominos


class Game:
    tetromino: Tetromino

    def __init__(self, display):
        self.rows = 22
        self.cols = 12
        self.wall_width = 1
        self.bottom_wall_width = 2
        self.game_map = None
        self.tetromino = None

        self.update_map_data = self.iter_tetromino_area(self.update_map_action)
        self.collide_detect = \
            self.iter_tetromino_area(self.collide_detect_action)

        self.game_over = False

        graphic.init_graphic(display, self.rows, self.cols)

    def iter_tetromino_area(self, action):

        def func():
            tetromino_array = \
                tetrominos[self.tetromino.tetromino_type][self.tetromino.orient]
            window_x0, window_x1, window_y0, window_y1 = \
                get_tetromino_area(self.tetromino.pos_x,
                                   self.tetromino.pos_y,
                                   self.tetromino.length)
            tetromino_x = 0
            for i in range(window_x0, window_x1):
                tetromino_y = self.tetromino.length - 1
                for j in range(window_y0, window_y1, -1):
                    if action(tetromino_array, j, i, tetromino_y, tetromino_x):
                        return True
                    tetromino_y -= 1
                tetromino_x += 1
            return False

        return func

    def update_map_action(self, tetromino_array, j, i, tetromino_y, tetromino_x):
        self.game_map[j][i] += \
            tetromino_array[tetromino_y][tetromino_x]

    def collide_detect_action(self, tetromino_array, j, i, tetromino_y, tetromino_x):
        if (self.game_map[j][i] +
                tetromino_array[tetromino_y][tetromino_x]) > 1:
            return True

    def update_map(self):
        self.update_map_data()
        graphic.diff_draw(self.game_map)

    def move_down(self):
        self.tetromino.pos_y_pre = self.tetromino.pos_y
        self.tetromino.pos_y += 1
        if self.collide_detect():
            self.tetromino.pos_y -= 1
            self.update_map()
            self.add_tetromino()
        graphic.draw_tetromino(self.tetromino)

    def move_right(self):
        self.tetromino.pos_x_pre = self.tetromino.pos_x
        self.tetromino.pos_x += 1
        if self.collide_detect():
            self.tetromino.pos_x -= 1

    def move_left(self):
        self.tetromino.pos_x_pre = self.tetromino.pos_x
        self.tetromino.pos_x -= 1
        if self.collide_detect():
            self.tetromino.pos_x += 1

    def add_tetromino(self):
        self.tetromino = Tetromino(self.cols)
        if self.collide_detect():
            self.game_over = True
        graphic.draw_tetromino(self.tetromino, clear_pre=False)

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
        graphic.diff_draw(self.game_map)
        graphic.draw_tetromino(self.tetromino, clear_pre=False)
        while not self.game_over:
            utime.sleep_ms(200)
            self.move_down()
