import graphic
import utime
from tetromino import Tetromino, tetrominos
import control


class Score:
    def __init__(self):
        self.score = 0
        self.rows = 0

    def add_score(self, level, rows):
        self.rows += rows
        if rows == 1:
            self.score += 40 * (level + 1)
        elif rows == 2:
            self.score += 100 * (level + 1)
        elif rows == 3:
            self.score += 300 * (level + 1)
        elif rows == 4:
            self.score += 1200 * (level + 1)


class Game:
    game_map: list[list] = None
    tetromino: Tetromino = None
    controller: control.Controller
    score: Score
    game_over: bool
    pause: bool

    def __init__(self, display):
        self.rows = 22
        self.cols = 12
        self.wall_width = 1
        self.bottom_wall_width = 2
        self.display = display
        self.speed = 100
        self.level = self.speed//100

        self.update_map = self.iter_tetromino_area(self.update_map)
        self.collide_detect = self.iter_tetromino_area(self.collide_detect)
        self.get_full_map = self.iter_tetromino_area(self.get_full_map)

    def iter_tetromino_area(self, action):

        def func(game_map):
            x = self.tetromino.length
            k = x
            pos_x = self.tetromino.pos_x
            pos_y = self.tetromino.pos_y
            tetromino_array = \
                tetrominos[self.tetromino.tetromino_type][self.tetromino.orient]
            if x > pos_y + 1:
                k = pos_y + 1
            if x + pos_x > self.cols:
                x -= 1
            for i in range(x):
                for j in range(k):
                    if action(tetromino_array, pos_y-j, pos_x+i, -j-1, i, game_map):
                        return True

        return func

    def update_map(self, tetromino_array, j, i, tetromino_y,
                   tetromino_x, game_map):
        game_map[j][i] += \
            tetromino_array[tetromino_y][tetromino_x]

    def collide_detect(self, tetromino_array, j, i, tetromino_y,
                       tetromino_x, game_map):
        if game_map[j][i] != 0 and tetromino_array[tetromino_y][tetromino_x] != 0:
            return True

    def get_full_map(self, tetromino_array, j, i, tetromino_y,
                     tetromino_x, game_map):
        if tetromino_array[tetromino_y][tetromino_x] != 0:
            game_map[j][i] = tetromino_array[tetromino_y][tetromino_x]

    def move_down(self):
        self.tetromino.pos_y += 1
        if self.collide_detect(self.game_map):
            self.tetromino.pos_y -= 1
            self.update_map(self.game_map)
            self.detect_and_remove_line()
            self.add_tetromino()
            return False
        return True

    def move_right(self):
        self.tetromino.pos_x += 1
        if self.collide_detect(self.game_map):
            self.tetromino.pos_x -= 1

    def move_left(self):
        self.tetromino.pos_x -= 1
        if self.collide_detect(self.game_map):
            self.tetromino.pos_x += 1

    def rotate(self):
        pre_orient = self.tetromino.orient
        if pre_orient == self.tetromino.type_variants - 1:
            self.tetromino.orient = -1
        self.tetromino.orient += 1
        if self.collide_detect(self.game_map):
            self.tetromino.orient = pre_orient

    def drop(self):
        while self.move_down():
            self.fresh_lcd()

    def detect_and_remove_line(self):
        row = 0
        for i in range(self.rows-2):
            line_sum = 0
            for j in range(1, self.cols-1):
                if self.game_map[i][j] != 0:
                    line_sum += 1
            if line_sum == self.cols-2:
                self.remove_line(i)
                row += 1
        self.score.add_score(self.level, row)

    def remove_line(self, row_num: int):
        for i in range(row_num, 0, -1):
            for j in range(1, self.cols - 1):
                self.game_map[i][j] = self.game_map[i-1][j]
        for j in range(1, self.cols - 1):
            self.game_map[0][j] = 0

    def add_tetromino(self):
        self.tetromino = Tetromino(self.cols)
        if self.collide_detect(self.game_map):
            self.game_over = True

    def init_map(self):
        game_map = \
            [[0 for col in range(self.cols)] for row in range(self.rows)]
        # draw wall
        for i in range(self.rows):
            game_map[i][0] = 8
            game_map[i][-1] = 8
        for j in range(self.cols):
            game_map[-2][j] = 8
            game_map[-1][j] = 8
        return game_map

    def init_game(self):
        self.game_map = self.init_map()
        self.add_tetromino()

        self.game_over = False
        self.pause = False
        self.score = Score()
        graphic.init_graphic(self.display, self.rows, self.cols)

    def fresh_lcd(self):
        full_map = [i.copy() for i in self.game_map]
        self.get_full_map(full_map)
        graphic.diff_draw(full_map)
        del full_map

    def set_controller(self, controller):
        self.controller = controller

    def start_game(self):
        self.init_game()

    def pause_game(self):
        self.pause = not self.pause

    def run(self):
        self.init_game()
        while True:
            counter = 0
            while not self.game_over and not self.pause:
                score_ = self.score.score

                utime.sleep_ms(1)
                if counter % self.speed == 0:
                    counter = 0
                    self.move_down()
                counter += 1

                self.controller.run()
                self.fresh_lcd()
                graphic.draw_img()

                if score_ != self.score.score:
                    score_ = self.score.score
                    graphic.draw_num(score_, graphic.score_pos_settings)
                    graphic.draw_num(self.score.rows, graphic.rows_pos_settings)
                    graphic.draw_img(celebrate=True)
