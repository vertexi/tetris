import machine

import graphic
import utime
from tetromino import get_tetromino_area, Tetromino, tetrominos
import joystick
from machine import Pin


class Game:
    tetromino: Tetromino

    def __init__(self, display):
        self.rows = 22
        self.cols = 12
        self.wall_width = 1
        self.bottom_wall_width = 2
        self.game_map = None
        self.tetromino = None
        self.drop_start_time = utime.ticks_ms()

        self.update_map_data = self.iter_tetromino_area(self.update_map_action)
        self.collide_detect = \
            self.iter_tetromino_area(self.collide_detect_action)

        self.game_over = False

        graphic.init_graphic(display, self.rows, self.cols)

    def iter_tetromino_area(self, action):

        def func():
            tetromino_array = \
                tetrominos[self.tetromino.tetromino_type][
                    self.tetromino.orient]
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

    def update_map_action(self, tetromino_array, j, i, tetromino_y,
                          tetromino_x):
        self.game_map[j][i] += \
            tetromino_array[tetromino_y][tetromino_x]

    def collide_detect_action(self, tetromino_array, j, i, tetromino_y,
                              tetromino_x):
        if (self.game_map[j][i]+tetromino_array[tetromino_y][tetromino_x]) > 1:
            return True

    def update_map(self):
        self.update_map_data()

    def get_full_map(self):
        full_map = [i.copy() for i in self.game_map]
        x = self.tetromino.length
        k = x
        pos_x = self.tetromino.pos_x
        pos_y = self.tetromino.pos_y
        tetromino_array = \
            tetrominos[self.tetromino.tetromino_type][self.tetromino.orient]
        if x > pos_y + 1:
            k = pos_y + 1
        for i in range(x):
            for j in range(k):
                if tetromino_array[-j - 1][i] == 1:
                    full_map[pos_y - j][pos_x + i] = 1
        return full_map

    def move_down(self):
        self.tetromino.pos_y += 1
        if self.collide_detect():
            self.tetromino.pos_y -= 1
            self.update_map()
            self.detect_and_remove_line()
            self.add_tetromino()
            return False
        return True

    def move_right(self):
        self.tetromino.pos_x += 1
        if self.collide_detect():
            self.tetromino.pos_x -= 1

    def move_left(self):
        self.tetromino.pos_x -= 1
        if self.collide_detect():
            self.tetromino.pos_x += 1

    def rotate(self, pin):
        pre_orient = self.tetromino.orient
        if pre_orient == self.tetromino.type_variants - 1:
            self.tetromino.orient = -1
        self.tetromino.orient += 1
        if self.collide_detect():
            self.tetromino.orient = pre_orient

    def drop(self, pin):
        if utime.ticks_diff(utime.ticks_ms(), self.drop_start_time) > 100:
            while self.move_down():
                graphic.diff_draw(self.get_full_map())
            self.drop_start_time = utime.ticks_ms()

    def detect_and_remove_line(self):
        for i in range(self.rows-2):
            line_sum = 0
            for j in range(1, self.cols-1):
                line_sum += self.game_map[i][j]
            if line_sum == self.cols-2:
                self.remove_line(i)

    def remove_line(self, row_num: int):
        for i in range(row_num, 0, -1):
            for j in range(1, self.cols - 1):
                self.game_map[i][j] = self.game_map[i-1][j]
        for j in range(1, self.cols - 1):
            self.game_map[0][j] = 0

    def add_tetromino(self):
        self.tetromino = Tetromino(self.cols)
        if self.collide_detect():
            self.game_over = True

    def init_map(self):
        game_map = \
            [[0 for col in range(self.cols)] for row in range(self.rows)]
        # draw wall
        for i in range(self.rows):
            game_map[i][0] = 1
            game_map[i][-1] = 1
        for j in range(self.cols):
            game_map[-2][j] = 1
            game_map[-1][j] = 1
        return game_map

    def init_game(self):
        self.game_map = self.init_map()
        self.add_tetromino()

    def reset(self, pin):
        machine.reset()

    def run(self):
        self.init_game()
        joystick.buttonB.irq(self.rotate, Pin.IRQ_FALLING)
        joystick.buttonA.irq(self.drop, Pin.IRQ_FALLING)
        joystick.buttonStart.irq(self.reset, Pin.IRQ_FALLING)

        counter = 0
        left_counter = 0
        right_counter = 0
        while not self.game_over:
            utime.sleep_ms(1)
            counter += 1
            if counter == 100:
                counter = 0
                self.move_down()
            stick_x = joystick.x_value()
            if stick_x < 0xFFF:
                if left_counter % 30 == 0:
                    left_counter = 0
                    self.move_left()
                left_counter += 1
            elif stick_x > 0xEFFF:
                if right_counter % 30 == 0:
                    right_counter = 0
                    self.move_right()
                right_counter += 1
            graphic.diff_draw(self.get_full_map())
