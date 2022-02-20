import math


def rgb565_to_rgb888(rgb565):
    return math.floor((rgb565>>11)/0b11111*255),\
           math.floor((rgb565&0b11111100000>>5)/0b11111*255),\
           math.floor((0xF182&0b11111)/0b11111*255)
