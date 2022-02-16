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


class JoystickEvent:
    def __init__(self, stick_pos_handle, great_than: bool, pos_threshold: int,
                 counter_threshold: int, callback_handle):
        self.counter = 0
        self.stick_pos_handle = stick_pos_handle
        self.stick_pos = self.stick_pos_handle()
        self.pos_threshold = pos_threshold
        self.counter_threshold = counter_threshold
        self.great_than = great_than
        self.callback_handle = callback_handle

    def event(self):
        self.stick_pos = self.stick_pos_handle()
        trigger = False
        if self.great_than:
            if self.stick_pos > self.pos_threshold:
                trigger = True
        else:
            if self.stick_pos < self.pos_threshold:
                trigger = True
        if trigger:
            if self.counter % self.counter_threshold == 0:
                self.counter = 0
                self.callback_handle()
            self.counter += 1


class Joystick:
    def __init__(self, *args):
        self.controls = []
        for arg in args:
            self.controls.append(JoystickEvent(*arg))

    def run(self):
        for control in self.controls:
            control.event()
