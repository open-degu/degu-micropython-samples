import time
import zcoap
import ujson
from machine import I2C
from sys import exit

# create an i2c on bus 1
i2c = I2C(1)

# Default I2C slave address
BMA400_I2CADDR = 0x15

# Common register
BMA400_CHIPID = 0x00
BMA400_ERR_REG = 0x02
BMA400_STATUS = 0x03
BMA400_TEMP = 0x11

# Accelerometer value
OUTX_L_XL = 0x04
OUTX_H_XL = 0x05
OUTY_L_XL = 0x06
OUTY_H_XL = 0x07
OUTZ_L_XL = 0x08
OUTZ_H_XL = 0x09

# Configuration register
BMA400_CONFIG_0 = 0x19 #mode
BMA400_CONFIG_1 = 0x1A #range + data-rate
BMA400_CONFIG_2 = 0x1B #filter

# Option
# mode
BMA400_SLEEP = 0x00
BMA400_L_POWER = 0x01
BMA400_NORMAL = 0x02
BMA400_RESERVED = 0x03
# range
BMA400_FS_2g = 0x00
BMA400_FS_4g = 0x40
BMA400_FS_8g = 0x80
BMA400_FS_16g = 0xC0
# data rate
BMA400_ODR_12 = 0x00
BMA400_ODR_25 = 0x06
BMA400_ODR_50 = 0x07
BMA400_ODR_100 = 0x08
BMA400_ODR_200 = 0x09
BMA400_ODR_400 = 0x0A
BMA400_ODR_800 = 0x0B

class BMA400:

    def __init__(self, address):
        self.address = address
        self.acc_config0 = BMA400_CONFIG_0
        self.acc_config1 = BMA400_CONFIG_1
        self.acc_config2 = BMA400_CONFIG_2
        self.axis_reg = []
        self.temp_reg = BMA400_TEMP
        self.accel_config()

    def accel_config(self):
        accel_write_data0 =    0x01
        buff_accel = bytes([self.acc_config0, accel_write_data0])
        i2c.writeto(self.address, buff_accel)
        time.sleep_us(10)
        accel_write_data1  = BMA400_FS_16g
        accel_write_data1 |= BMA400_ODR_200
        buff_accel = bytes([self.acc_config1, accel_write_data1])
        i2c.writeto(self.address, buff_accel)

    def accel_axis_read(self):
        self.axis_reg = []
        self.axis_reg.extend([OUTX_L_XL, OUTX_H_XL, OUTY_L_XL, OUTY_H_XL, OUTZ_L_XL, OUTZ_H_XL])
        return self._axis_read_()

    def _axis_read_(self):
        # read register's data
        global axis_x
        axis_x = 0
        global axis_y
        axis_y = 0
        global axis_z
        axis_z = 0
        # read axis-x
        i2c.writeto(self.address, self.axis_reg[0])
        byte_x_lsb = i2c.readfrom(self.address, 1)
        i2c.writeto(self.address, self.axis_reg[1])
        byte_x_msb = i2c.readfrom(self.address, 1)

        int_x_lsb = int.from_bytes(byte_x_lsb, 'big')
        int_x_msb = int.from_bytes(byte_x_msb, 'big')
        # read axis-y
        i2c.writeto(self.address, self.axis_reg[2])
        byte_y_lsb = i2c.readfrom(self.address, 1)
        i2c.writeto(self.address, self.axis_reg[3])
        byte_y_msb = i2c.readfrom(self.address, 1)

        int_y_lsb = int.from_bytes(byte_y_lsb, 'big')
        int_y_msb = int.from_bytes(byte_y_msb, 'big')
        # read axis-z
        i2c.writeto(self.address, self.axis_reg[4])
        byte_z_lsb = i2c.readfrom(self.address, 1)
        i2c.writeto(self.address, self.axis_reg[5])
        byte_z_msb = i2c.readfrom(self.address, 1)

        int_z_lsb = int.from_bytes(byte_z_lsb, 'big')
        int_z_msb = int.from_bytes(byte_z_msb, 'big')

        # combine to 16bit - unsigned type
        axis_x = int_x_msb<<8 | int_x_lsb
        axis_y = int_y_msb<<8 | int_y_lsb
        axis_z = int_z_msb<<8 | int_z_lsb

        # signed data
        if axis_x > 2047:
            axis_x -= 4096
        if axis_y > 2047:
            axis_y -= 4096
        if axis_z > 2047:
            axis_z -= 4096

        # convert to g
        x = round(((axis_x * 7.81)/1000), 2)
        y = round(((axis_y * 7.81)/1000), 2)
        z = round(((axis_z * 7.81)/1000), 2)

        return {'x': x, 'y': y, 'z': x}

    def temprature_read(self): 
        global temp_data
        temp_data = 0
        i2c.writeto(self.address, self.temp_reg)
        temp_data = i2c.readfrom(self.address, 1)
        temp_int = int.from_bytes(temp_data, 'big')

        if(temp_int > 127):
            temp_int -= 255

        temp = ((temp_int*0.5) + 23)
        return temp

    def _check_setup_reg_(self):
        i2c.writeto(self.address, self.accel_config0)
        temp1 = i2c.readfrom(self.address, 1)
        print("CONFIG0: ", bin(int.from_bytes(temp1, 'big')))
        time.sleep_us(10)

        i2c.writeto(self.address, CTRL2_G)
        temp2 = i2c.readfrom(self.acc_config1, 1)
        print("CONFIG1: ", bin(int.from_bytes(temp2, 'big')))
        time.sleep_us(10)

def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    bma400 = BMA400(BMA400_I2CADDR)

    while True:
        reported['state']['reported']['temp'] = bma400.temprature_read()
        reported['state']['reported']['axis'] = bma400.accel_axis_read()

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(5)

if __name__ == "__main__":
    main()
