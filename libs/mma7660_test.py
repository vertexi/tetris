from machine import Pin, I2C
from libs import mma7660
import utime

i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=400000)
print(i2c)
accel = mma7660.Accelerometer(i2c)
while True:
#     print(accel.getXYZ(), accel.get_x(), accel.get_y(), accel.get_z())
    print(accel.getAcceleration(), accel.getAcceleration_x(), accel.getAcceleration_y(), accel.getAcceleration_z())
#     print(accel.getAngle())
    utime.sleep_ms(500)