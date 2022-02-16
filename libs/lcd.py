import time
import st7789


def dis_init(spi, reset=None, dc=None, cs=None, backlight=None):
    if spi is None:
        raise ValueError(
                "spi is None"
                )
    if cs:
        cs.off()
    dc.on()
    spi.write(bytes(0xFF))
    if cs:
        cs.on()

    if cs:
        cs.off()
    if reset:
        reset.on()
    time.sleep_ms(50)
    if reset:
        reset.off()
    time.sleep_ms(50)
    if reset:
        reset.on()
    time.sleep_ms(150)
    if cs:
        cs.on()


def lcd_config(spi, width=240, height=240, reset=None, dc=None, rotation=0):
    dis_init(spi, reset=reset, dc=dc)
    display = st7789.ST7789(spi, width, height, reset=reset, dc=dc,
                            rotation=rotation)
    display.init()
    display.fill(st7789.BLACK)
    return display
