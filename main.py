import gc
import machine
from machine import Pin
from libs import lcd
import uos


gc.collect()
spi_sck = machine.Pin(2, machine.Pin.OUT)
spi_tx = machine.Pin(3, machine.Pin.OUT)
lcd_reset = machine.Pin(0, machine.Pin.OUT)
lcd_dc = machine.Pin(1, machine.Pin.OUT)
spi_lcd = machine.SPI(0, baudrate=80000000, phase=1, polarity=1, sck=spi_sck, mosi=spi_tx)
display = lcd.lcd_config(spi_lcd, width=240, height=240, reset=lcd_reset, dc=lcd_dc, rotation=0)
display.init()

