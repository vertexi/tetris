from machine import Pin, ADC

xAxis = ADC(Pin(29))
yAxis = ADC(Pin(28))

buttonB = Pin(5, Pin.IN, Pin.PULL_UP)  # B
buttonA = Pin(6, Pin.IN, Pin.PULL_UP)  # A
buttonStart = Pin(7, Pin.IN, Pin.PULL_UP)
buttonSelect = Pin(8, Pin.IN, Pin.PULL_UP)


def x_value():
    return xAxis.read_u16()


def y_value():
    return yAxis.read_u16()


def button_a():
    return buttonA.value()


def button_b():
    return buttonB.value()


def button_start():
    return buttonStart.value()


def button_select():
    return buttonSelect.value()
