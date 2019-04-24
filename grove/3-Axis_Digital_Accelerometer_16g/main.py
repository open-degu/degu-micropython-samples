import time
import zcoap
import ujson
import machine
from sys import exit

i2c = machine.I2C(1)

# Default I2C slave address
ADXL345_I2CADDR = 0x53

ADXL345_DATA_FORMAT = 0x31
ADXL345_BW_RATE      = 0x2C
POWER_CTL            = 0x2D

ADXL345_BW_RATE1600HZ      = 0x0F
ADXL345_BW_RATE800HZ       = 0x0E
ADXL345_BW_RATE400HZ       = 0x0D
ADXL345_BW_RATE200HZ       = 0x0C
ADXL345_BW_RATE100HZ       = 0x0B
ADXL345_BW_RATE50HZ        = 0x0A
ADXL345_BW_RATE25HZ        = 0x09

ADXL345_FS_2g       = 0x00
ADXL345_FS_4g       = 0x01
ADXL345_FS_8g       = 0x02
ADXL345_FS_16g      = 0x03

MEASURE             = 0x08
AXES_DATA           = 0x32

class ADXL345:
    def __init__(self, address):
        self.address = address
        self.setBandwidthRate(ADXL345_BW_RATE100HZ)
        self.setRange(ADXL345_FS_16g)
        self.enableMeasurement()

    def enableMeasurement(self):
        buff_ = bytes([POWER_CTL, MEASURE])
        i2c.writeto(self.address, buff_)

    def setBandwidthRate(self, rate_flag):
        buff_accel = bytes([ADXL345_BW_RATE, rate_flag])
        i2c.writeto(self.address, buff_accel)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        i2c.writeto(self.address, ADXL345_DATA_FORMAT)
        data_ = i2c.readfrom(self.address, 1)
        value = int.from_bytes(data_, 'big')
        value &= ~0x0F;
        value |= range_flag;
        value |= 0x08;
        buff_accel = bytes([ADXL345_DATA_FORMAT, value])
        i2c.writeto(self.address, buff_accel)

    def getAxes(self):
        global axis_x
        axis_x = 0
        global axis_y
        axis_y = 0
        global axis_z
        axis_z = 0

        i2c.writeto(self.address, AXES_DATA)
        bytes = i2c.readfrom(self.address, 6)

        axis_x = bytes[0] | (bytes[1] << 8)
        axis_y = bytes[2] | (bytes[3] << 8)
        axis_z = bytes[4] | (bytes[5] << 8)

        # signed data
        if axis_x > 32767:
            axis_x -= 65536
        if axis_y > 32767:
            axis_y -= 65536
        if axis_z > 32767:
            axis_z -= 65536

        x = round(((axis_x * 4)/1000), 2)
        y = round(((axis_y * 4)/1000), 2)
        z = round(((axis_z * 4)/1000), 2)

        return {'x': x, 'y': y, 'z': z}

def main():
    path = 'thing/' + zcoap.eui64()
    reported = {'state':{'reported':{}}}

    addr = zcoap.gw_addr()
    port = 5683
    cli = zcoap.client((addr, port))

    adxl345 = ADXL345(ADXL345_I2CADDR)

    while True:
        reported['state']['reported']['axis'] = adxl345.getAxes()

        print(ujson.dumps(reported))
        cli.request_post(path, ujson.dumps(reported))
        time.sleep(5)

if __name__ == "__main__":
    main()
