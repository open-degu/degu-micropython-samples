import time
import degu
import ujson
import machine

i2c = machine.I2C(1)

# Default I2C slave address
MMC7660_I2CADDR = 0x4C

# common value
MMC7660_LS_X = 0x00
MMC7660_LS_Y = 0x01
MMC7660_LS_Z = 0x02

MMC7660_TILT = 0x03
MMC7660_MODE = 0x07

STANDBY_MODE = 0x00
TEST_MODE    = 0x04
ACTIVE_MODE  = 0x01

class MMC7660:
    def __init__(self, address):
        self.address  = address
        self.mmc7660_config(MMC7660_MODE)

    def mmc7660_config(self, mode_register):
        # mode
        data_buff = bytes([mode_register, ACTIVE_MODE])
        i2c.writeto(self.address, data_buff)
        # 
    def getAxes(self):
        global axis_x
        axis_x = 0
        global axis_y
        axis_y = 0
        global axis_z
        axis_z = 0

        i2c.writeto(self.address, MMC7660_LS_X)
        bytes = i2c.readfrom(self.address, 3)
        
        axis_x = bytes[0]
        axis_y = bytes[1]
        axis_z = bytes[2]

        # signed data
        if axis_x > 31:
            axis_x -= 64
        if axis_y > 31:
            axis_y -= 64
        if axis_z > 31:
            axis_z -= 64

        x = round(((axis_x * 46)/1000), 2)
        y = round(((axis_y * 46)/1000), 2)
        z = round(((axis_z * 46)/1000), 2)

        return {'x': x, 'y': y, 'z': z}

def main():
    reported = {'state':{'reported':{}}}

    mmc7660 = MMC7660(MMC7660_I2CADDR)

    while True:
        reported['state']['reported']['axis'] = mmc7660.getAxes()

        json = ujson.dumps(reported)
        print(json)
        degu.update_shadow(json)
        time.sleep(5)

if __name__ == "__main__":
    main()

