import math
import st7789
from tetromino import get_tetromino_area, Tetromino, tetrominos

tetromino_width = 0
prev_map: list[list] = None
display: st7789.ST7789 = None
game_rows:int = 0
game_cols:int = 0


def init_graphic(display_: st7789.ST7789, game_rows_, game_cols_):
    global display
    global tetromino_width
    global prev_map
    global game_rows
    global game_cols
    game_rows = game_rows_
    game_cols = game_cols_
    display = display_
    tetromino_width = eval_tetromino_shape(game_rows, display.height())
    prev_map = init_prev_map(game_cols, game_rows)


def eval_tetromino_shape(map_rows, lcd_height):
    tetromino_width_ = math.floor(lcd_height/map_rows)
    return tetromino_width_


def copy_map(game_map: list[list]):
    new_map = [i.copy() for i in game_map]
    return new_map


def init_prev_map(cols, rows):
    prev_map_ = [[0 for col in range(cols)] for row in range(rows)]
    return prev_map_


def diff_draw(game_map: list[list]):
    global prev_map
    for i in range(game_rows):
        for j in range(game_cols):
            diff = prev_map[i][j] - game_map[i][j]
            if diff == 0:
                pass
            else:
                if diff == 1:
                    draw_block(j, i, st7789.BLACK)
                elif diff == -1:
                    draw_block(j, i, st7789.WHITE)
    prev_map = copy_map(game_map)


def draw_tetromino(tetromino: Tetromino, clear_pre=True):
    if clear_pre:
        tetromino_array = tetrominos[tetromino.tetromino_type][tetromino.orient_pre]
        window_x0, window_x1, window_y0, window_y1 = \
            get_tetromino_area(tetromino.pos_x_pre,
                               tetromino.pos_y_pre,
                               tetromino.length)
        tetromino_x = 0
        for i in range(window_x0, window_x1):
            tetromino_y = tetromino.length - 1
            for j in range(window_y0, window_y1, -1):
                if tetromino_array[tetromino_y][tetromino_x] == 1:
                    draw_block(i, j, st7789.BLACK)
                tetromino_y -= 1
            tetromino_x += 1

    tetromino_array = tetrominos[tetromino.tetromino_type][tetromino.orient]
    window_x0, window_x1, window_y0, window_y1 = \
        get_tetromino_area(tetromino.pos_x,
                           tetromino.pos_y,
                           tetromino.length)
    tetromino_x = 0
    for i in range(window_x0, window_x1):
        tetromino_y = tetromino.length - 1
        for j in range(window_y0, window_y1, -1):
            if tetromino_array[tetromino_y][tetromino_x] == 1:
                draw_block(i, j, st7789.WHITE)
            tetromino_y -= 1
        tetromino_x += 1


def draw_block(x: int, y: int, color: int):
    x *= tetromino_width
    y *= tetromino_width
    display.fill_rect(x, y, tetromino_width, tetromino_width, color)
