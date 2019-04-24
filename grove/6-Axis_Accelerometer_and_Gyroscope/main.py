import time
import zcoap
import ujson
from machine import I2C
from sys import exit

#create an i2c on bus 1
i2c = I2C(1)

# Common value
WHO_AM_I    = 0x0F
CTRL1_XL    = 0X10
CTRL2_G        = 0x11
DEVICE_ADDR     = 0x6A

# Accelerometer value
OUTX_L_XL      = 0x28
OUTX_H_XL      = 0x29

OUTY_L_XL      = 0x2A
OUTY_H_XL      = 0x2B

OUTZ_L_XL      = 0x2C
OUTZ_H_XL      = 0x2D
# Configuration register
BW_XL_100Hz    = 0x02
FS_XL_16g    = 0x04
ODR_XL_104Hz    = 0x40

# ///gyroscopemeter///
OUTX_L_G    = 0x22
OUTX_H_G    = 0x23

OUTY_L_G    = 0x24
OUTY_H_G    = 0x25

OUTZ_L_G    = 0x26
OUTZ_H_G    = 0x27

# configuration register
FS_G_1000dps    = 0x08
ODR_G_104Hz    = 0x40

class LSM6DS3:

    def __init__(self, address, accel_mode=False, gyros_mode=False):
        self.address     = address
        self.accel_mode = accel_mode
        self.gyros_mode = gyros_mode
        self.axis_reg    = []

    def accel_start(self):
        if not self.accel_mode:
            pass
        else:
            accel_write = 0
            accel_write |= FS_XL_16g
            accel_write |= BW_XL_100Hz
            accel_write |= ODR_XL_104Hz

            buff_accel = bytes([CTRL1_XL, accel_write])
            i2c.writeto(self.address, buff_accel)
            return self.accel_axis_read()

    def accel_axis_read(self):
        self.axis_reg = []
        self.axis_reg.extend([OUTX_L_XL, OUTX_H_XL, OUTY_L_XL, OUTY_H_XL, OUTZ_L_XL, OUTZ_H_XL])
        return self._axis_read_(True)

    def gyros_start(self):
        if not self.gyros_mode:
            pass
        else:
            gyro_write    = 0
            gyro_write    |= FS_G_1000dps
            gyro_write    |= ODR_G_104Hz

            buff_gyro = bytes([CTRL2_G, gyro_write])
            i2c.writeto(self.address, buff_gyro)
            time.sleep_us(10)
            return self.gyros_axis_read()

    def gyros_axis_read(self):
        self.axis_reg = []
        self.axis_reg.extend([OUTX_L_G, OUTX_H_G, OUTY_L_G, OUTY_H_G, OUTZ_L_G, OUTZ_H_G])
        return self._axis_read_(False)
    
    def _axis_read_(self, select_accel):        
        # Read data from assigned registers
        global axis_x
        axis_x = 0
        global axis_y
        axis_y = 0
        global axis_z
        axis_z = 0

        # read accelero x
        i2c.writeto(self.address, self.axis_reg[0])
        byte_x_lsb = i2c.readfrom(self.address, 1)
        i2c.writeto(self.address, self.axis_reg[1])
        byte_x_msb = i2c.readfrom(self.address, 1)

        int_x_lsb = int.from_bytes(byte_x_lsb, 'big')
        int_x_msb = int.from_bytes(byte_x_msb, 'big')
        # read accelero y
        i2c.writeto(self.address, self.axis_reg[2])
        byte_y_lsb = i2c.readfrom(self.address, 1)
        i2c.writeto(self.address, self.axis_reg[3])
        byte_y_msb = i2c.readfrom(self.address, 1)

        int_y_lsb = int.from_bytes(byte_y_lsb, 'big')
        int_y_msb = int.from_bytes(byte_y_msb, 'big')
        # read accelero z
        i2c.writeto(self.address, self.axis_reg[4])
        byte_z_lsb = i2c.readfrom(self.address, 1)
        i2c.writeto(self.address, self.axis_reg[5])
        byte_z_msb = i2c.readfrom(self.address, 1)

        int_z_lsb = int.from_bytes(byte_z_lsb, 'big')
        int_z_msb = int.from_bytes(byte_z_msb, 'big')

        # conbine to 16bit - unsigned type
        axis_x = int_x_msb<<8 | int_x_lsb
        axis_y = int_y_msb<<8 | int_y_lsb
        axis_z = int_z_msb<<8 | int_z_lsb

        # signed data
        if axis_x > 0x7FFF:
            axis_x -= 0x10000
        if axis_y > 0x7FFF:
            axis_y -= 0x10000
        if axis_z > 0x7FFF:
            axis_z -= 0x10000

        if select_accel:
            x = ((axis_x * 0.488)/1000)
            y = ((axis_y * 0.488)/1000)
            z = ((axis_z * 0.488)/1000)
        else:
            x = ((axis_x * 35)/1000)
            y = ((axis_y * 35)/1000)
            z = ((axis_z * 35)/1000)

        return {'x': x, 'y': y, 'z': z}

    def _check_setup_reg_(self):
        i2c.writeto(self.address, CTRL1_XL)
        temp1 = i2c.readfrom(self.address, 1)
        print("CTRL1_XL: ", bin(int.from_bytes(temp1, 'big')))
        time.sleep_us(10)

        i2c.writeto(self.address, CTRL2_G)
        temp2 = i2c.readfrom(self.address, 1)
        print("CTRL2_G:  ", bin(int.from_bytes(temp2, 'big')))
        time.sleep_us(10)

def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    lsm6ds3 = LSM6DS3(0x6A, True, True) #device_addr, accel_mode, gyros_mode

    while True:
        reported['state']['reported']['accel'] = lsm6ds3.accel_start()
        reported['state']['reported']['gyro'] = lsm6ds3.gyros_start()

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(5)

if __name__ == "__main__":
    main()
