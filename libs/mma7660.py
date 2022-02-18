from machine import I2C
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

    def __init__(self, i2c: I2C, interrupts=False):
        self.i2c = i2c

        self.initAccelTable()
        self.setMode(MMA7660_STAND_BY)
        self.setSampleRate(AUTO_SLEEP_120)

        if interrupts:
            self.write(MMA7660_INTSU, interrupts)

        self.setMode(MMA7660_ACTIVE | MMA7660_AUTO_SLEEP_ENABLE)
        self.get_x = self.get_val_decorator(self.get_x)
        self.get_y = self.get_val_decorator(self.get_y)
        self.get_z = self.get_val_decorator(self.get_z)

        for i in range(5):
            self.getXYZ()

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
        for i in range(63, 31, -1):
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
        for i in range(63, 42, -1):
            self.accLookup[i].xyAngle = val
            self.accLookup[i].zAngle = valZ
            val -= 2.69
            valZ += 2.69

        for i in range(22, 43):
            self.accLookup[i].xyAngle = 255
            self.accLookup[i].zAngle = 255

    def setMode(self, mode):
        self.write(MMA7660_MODE, mode)

    def setSampleRate(self, rate):
        self.write(MMA7660_SR, rate)

    def getXYZ(self):
        count = 0
        val = [64, 64, 64]
        while count < 3:
            while val[count] > 63:
                val[count] = int.from_bytes(self.read(count, 1), 'little')  # 0x00 0x01 0x03 x y z
            count += 1
        return val

    def get_val_decorator(self, func):
        def get_val():
            val = 64
            while val > 63:
                val = func()
            return val

        return get_val

    def get_x(self):
        return int.from_bytes(self.read(MMA7660_X, 1), 'little')

    def get_y(self):
        return int.from_bytes(self.read(MMA7660_Y, 1), 'little')

    def get_z(self):
        return int.from_bytes(self.read(MMA7660_Z, 1), 'little')

    def getAcceleration(self):
        x, y, z = self.getXYZ()
        return self.accLookup[x].g, self.accLookup[y].g, self.accLookup[z].g

    def getAcceleration_x(self):
        x = self.get_x()
        return self.accLookup[x].g

    def getAcceleration_y(self):
        y = self.get_y()
        return self.accLookup[y].g

    def getAcceleration_z(self):
        z = self.get_z()
        return self.accLookup[z].g

    def getAngle(self):
        x, y, z = self.getXYZ()
        return self.accLookup[x].xyAngle, self.accLookup[y].xyAngle, self.accLookup[z].zAngle

    def getAllData(self):
        data = MMA7660_DATA()
        count = 0
        val = []
        while count < 11:
            val.append(self.read(count, 1))  # 0x00 0x01 0x03 x y z
            count += 1
        data.X = val[0]
        data.Y = val[1]
        data.Z = val[2]
        data.TILT = val[3]
        data.SRST = val[4]
        data.SPCNT = val[5]
        data.INTSU = val[6]
        data.MODE = val[7]
        data.SR = val[8]
        data.PDET = val[9]
        data.PD = val[10]
        return data
