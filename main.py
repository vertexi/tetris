import gc
import machine
from machine import Pin
from libs import lcd
from tetris import Game


# initialize
machine.freq(240000000)
gc.collect()

# init lcd
spi_sck = Pin(2, Pin.OUT)
spi_tx = Pin(3, Pin.OUT)
lcd_reset = Pin(0, Pin.OUT)
lcd_dc = Pin(1, Pin.OUT)
lcd_width = 240
lcd_height = 240
spi_lcd = machine.SPI(0, baudrate=40000000, phase=1, polarity=1,
                      sck=spi_sck, mosi=spi_tx)
display = lcd.lcd_config(spi_lcd, width=lcd_width, height=lcd_height,
                         reset=lcd_reset, dc=lcd_dc, rotation=0)

game = Game(display)
game.run()
