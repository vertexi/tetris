import gc
import machine
import st7789
from machine import Pin
from libs import lcd


# initialize
gc.collect()

# init lcd
spi_sck = Pin(2, Pin.OUT)
spi_tx = Pin(3, Pin.OUT)
lcd_reset = Pin(0, Pin.OUT)
lcd_dc = Pin(1, Pin.OUT)
spi_lcd = machine.SPI(0, baudrate=40000000, phase=1, polarity=1,
                      sck=spi_sck, mosi=spi_tx)
display = lcd.lcd_config(spi_lcd, width=240, height=240, reset=lcd_reset,
                         dc=lcd_dc, rotation=0)
display.init()

display.fill(st7789.WHITE)
