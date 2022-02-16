import math
import st7789
import italiccs
import scriptc

tetromino_width = 0
prev_map: list[list]
display: st7789.ST7789
game_rows: int = 0
game_cols: int = 0
display_height: int

score_pos_settings: dict
rows_pos_settings: dict


def init_graphic(display_: st7789.ST7789, game_rows_, game_cols_):
    global display
    global tetromino_width
    global prev_map
    global game_rows
    global game_cols
    global display_height
    global score_pos_settings
    global rows_pos_settings

    game_rows = game_rows_
    game_cols = game_cols_
    display = display_
    display_height = display.height()
    tetromino_width = eval_tetromino_shape(game_rows, display_height)
    prev_map = init_prev_map(game_cols, game_rows)
    display.fill(st7789.BLACK)

    score_pos_settings = draw_score_setting("Score", 5/8, 1/8, 0xe7e0, 5, 0xece0)
    display.draw(italiccs, "Score", score_pos_settings["text_x"],
                 score_pos_settings["text_y"], score_pos_settings["text_color"])
    draw_num(0, score_pos_settings)
    rows_pos_settings = draw_score_setting("Rows", 5/8, 3/8, 0xe7e0, 4, 0xece0)
    display.draw(italiccs, "Rows", rows_pos_settings["text_x"],
                 rows_pos_settings["text_y"], rows_pos_settings["text_color"])
    draw_num(0, rows_pos_settings)


def draw_score_setting(text, text_frac_x, text_frac_y, text_color, num_num, num_color):
    text_x = math.floor(display_height*text_frac_x)
    text_y = math.floor(display_height*text_frac_y)
    text_center = display.draw_len(italiccs, text)//2 + text_x
    num_y = text_y + italiccs.HEIGHT + 2
    num_len = display.draw_len(scriptc, "0")
    num_clear_x = text_center - num_len * 2
    num_clear_y = num_y - 13
    num_clear_width = num_len * num_num
    num_clear_height = scriptc.HEIGHT + 2
    score_pos_setting = {"text_x": text_x, "text_y": text_y, "text_color": text_color,
                         "text_center": text_center, "num_y": num_y, "num_len": num_len,
                         "num_clear_x": num_clear_x, "num_clear_y": num_clear_y,
                         "num_clear_width": num_clear_width, "num_clear_height": num_clear_height,
                         "num_color": num_color}
    return score_pos_setting


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
                prev_map[i][j] = game_map[i][j]
                if diff == 1:
                    draw_block(j, i, st7789.BLACK)
                elif diff == -1:
                    draw_block(j, i, st7789.WHITE)


def draw_block(x: int, y: int, color: int):
    x *= tetromino_width
    y *= tetromino_width
    display.fill_rect(x, y, tetromino_width, tetromino_width, color)


def draw_num(num: int, setting: dict):
    display.fill_rect(setting["num_clear_x"], setting["num_clear_y"],
                      setting["num_clear_width"], setting["num_clear_height"],
                      st7789.BLACK)
    num_x = setting["text_center"]-setting["num_len"]*len(str(num))//2
    display.draw(scriptc, str(num), num_x, setting["num_y"], setting["num_color"])
