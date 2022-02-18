from machine import I2C
from machine import Pin
from micropython import const


MMA7660_ADDR = const(0x4c)
MMA7660TIMEOUT = const(500)

MMA7660_X = const(0x00)
MMA7660_Y = const(0x01)
MMA7660_Z = const(0x02)
MMA7660_TILT = const(0x03)
MMA7660_SRST = const(0x04)
MMA7660_SPCNT = const(0x05)
MMA7660_INTSU = const(0x06)
MMA7660_SHINTX = const(0x80)
MMA7660_SHINTY = const(0x40)
MMA7660_SHINTZ = const(0x20)
MMA7660_GINT = const(0x10)
MMA7660_ASINT = const(0x08)
MMA7660_PDINT = const(0x04)
MMA7660_PLINT = const(0x02)
MMA7660_FBINT = const(0x01)
MMA7660_MODE = const(0x07)
MMA7660_STAND_BY = const(0x00)
MMA7660_ACTIVE = const(0x01)
MMA7660_AUTO_SLEEP_ENABLE = const(0b00010000)
MMA7660_SR = const(0x08)  # sample rate register
AUTO_SLEEP_120 = const(0X00)  # 120 sample per second
AUTO_SLEEP_64 = const(0X01)
AUTO_SLEEP_32 = const(0X02)
AUTO_SLEEP_16 = const(0X03)
AUTO_SLEEP_8 = const(0X04)
AUTO_SLEEP_4 = const(0X05)
AUTO_SLEEP_2 = const(0X06)
AUTO_SLEEP_1 = const(0X07)
MMA7660_PDET = const(0x09)
MMA7660_PD = const(0x0A)


class MMA7660_DATA:
    def __init__(self):
        self.X = None
        self.Y = None
        self.Z = None
        self.TILT = None
        self.SRST = None
        self.SPCNT = None
        self.INTSU = None
        self.MODE = None
        self.SR = None
        self.PDET = None
        self.PD = None


class MMA7660_LOOKUP:
    def __init__(self):
        self.g: int = 0
        self.xyAngle: int = 0
        self.zAngle: int = 0

class Accelerometer:
    accLookup: list[MMA7660_LOOKUP] = [MMA7660_LOOKUP() for i in range(64)]

    def __init__(self, scl: Pin, sda: Pin, interrupts=False):

        self.i2c = I2C(0, scl=scl, sda=sda, freq=400000)
        self.i2c.init()

        self.initAccelTable()
        self.setMode(MMA7660_STAND_BY)
        self.setSampleRate(AUTO_SLEEP_32)

        if interrupts:
            self.write(MMA7660_INTSU, interrupts)

        self.setMode(MMA7660_ACTIVE)

    def write(self, register: int, data):
        data = bytearray([data])
        self.i2c.writeto_mem(MMA7660_ADDR, register, data)

    def read(self, register: int, nbytes: int):
        buf = self.i2c.readfrom_mem(MMA7660_ADDR, register, nbytes)
        return buf

    def initAccelTable(self):
        val = 0
        for i in range(32):
            self.accLookup[i].g = val
            val += 0.047

        val = -0.047
        for i in range(63,31,-1):
            self.accLookup[i].g = val
            val -= 0.047

        val = 0
        valZ = 90
        for i in range(22):
            self.accLookup[i].xyAngle = val
            self.accLookup[i].zAngle = valZ
            val -= 2.69
            valZ += 2.69

        val = -2.69
        valZ = -87.31
        for i in range(63, 42,-1):
            self.accLookup[i].xyAngle = val
            self.accLookup[i].zAngle = valZ
            val -= 2.69
            valZ += 2.69

        for i in range(22,43):
            self.accLookup[i].xyAngle = 255
            self.accLookup[i].zAngle = 255

    def setMode(self, mode):
        self.write(MMA7660_MODE, mode)

    def setSampleRate(self, rate):
        self.write(MMA7660_SR, rate)

    def getXYZ(self):
        count = 0
        val = [64,64,64]
        while count < 3:
            while val[count] > 63:
                val[count] = self.read(count, 1)  # 0x00 0x01 0x03 x y z
            count += 1
        return  val
    #
    #
    #
    #
    #
    #     return data = (x,y,z)
    #
    # def getAcceleration(self):
    #     return True
    #     return False
    #
    # def getAllData(self):
    #     count = 0
    #
    #
    #
    #     return True
    #     return False
